# encoding: utf-8
import requests
from bs4 import BeautifulSoup
import re
from allabolag.utils import _dl_to_dict, _table_to_dict, _prefix_keys
from allabolag.parsers import PARSERS

class Company():
    """Represents a single company.

    Usage:
        c = Company("559006-6642")
        print(c.data) # get all cleaned data
        print(c.raw_data) # get all uncleaned data
    """
    def __init__(self, company_code):
        self.company_code = company_code
        self.url = "https://www.allabolag.se/{}".format(company_code.replace("-",""))
        self._data = {}
        self._overview_data = {}
        self._activity_data = {}
        self._accounts_data = {}

    @property
    def raw_data(self):
        """Get data from all sections
        """
        data = {}
        data.update(self.overview_data)
        data.update(self.activity_data)
        data.update(self.accounts_data)

        return data

    @property
    def data(self):
        return self._clean_data(self.raw_data)


    @property
    def overview_data(self):
        """Collect data from 'Översikt'
        """
        if self._overview_data == {}:
            s = self._get_soup()
            data = {
                "Namn": s.select_one("h1").text.strip(),

            }

            # Parse "Information" box
            information_elem = s.find(text="Information").parent.parent
            info_list = information_elem.select_one("dl")
            information = _dl_to_dict(info_list)
            data.update(information)

            # Parse "Kontaktuppgifter" box
            elem = s.find(text="Kontaktuppgifter").parent.parent
            dl = elem.select_one("dl")
            contacts = _dl_to_dict(dl)
            data.update(contacts)

            # Parse "Nyckeltal"
            account_fig_summary_soup = s.select_one(".company-account-figures")
            if account_fig_summary_soup is not None:
                data["account_figures_year"] = account_fig_summary_soup.select_one("h2").text.strip()
                account_fig_table =  account_fig_summary_soup.select_one("table")
                keys = [x.text.strip() for x in account_fig_table.select("th")]
                values = [x.text.strip() for x in account_fig_table.select("td")]
                account_figures = dict(zip(keys, values))
                data.update(account_figures)
            data = _prefix_keys(data, u"Översikt")

            self._overview_data = data

        return self._overview_data

    @property
    def activity_data(self):
        """Collect data from "Verksamhet & status"
        """
        if self._activity_data == {}:
            s = self._get_soup("verksamhet")
            data = {}

            # hova in alla dt-dd-taggar
            for dl in s.select("dl"):
                data.update(_dl_to_dict(dl))

            # "Verksamhet & ändamål" följer annan struktur (h3 + initliggande tagg)
            verksamhet_header = s.find(text=re.compile(u"^.*Verksamhet & ändamål.*"))
            if verksamhet_header:
                data[u"Verksamhet & ändamål"] = verksamhet_header.parent.find_next_sibling().text.strip()

            # SNI-koden ligger som kod (dt) + etikett (dd)
            sni_dl = s.select_one(".accordion-body.sni")
            if sni_dl:
                if sni_dl.select_one("dt"):
                    data[u"SNI-kod"] = sni_dl.select_one("dt").text.strip()
                    data[u"SNI-bransch"] = sni_dl.select_one("dd").text.strip()

            data = _prefix_keys(data, "Aktivitet och status")

            self._activity_data = data

        return self._activity_data

    @property
    def accounts_data(self):
        """Collect data from "Bokslut & nyckeltal" """
        if self._accounts_data == {}:
            data = {}
            s = self._get_soup("bokslut")
            for table in s.select("table"):
                #print _table_to_dict(table)
                table_caption = table.select_one("thead th.company-table__pager-button-cell").text.strip()
                if table_caption != u"Nyckeltal":
                    table_data = _table_to_dict(table)
                    table_data = _prefix_keys(table_data, table_caption)
                    data.update(table_data)
                else:
                    # Nyckeltal behöver egen parsing
                    # Hack Nyckeltalstabellen saknar år, därför tar vi dem från föregående år
                    years = [x[0] for x in list(table_data.values())[0]]

                    table_data = {}
                    for tr in table.select("tbody tr"):
                        try:
                            # Celler med
                            key = tr.select_one("span.row-title > span.tooltip > span").text
                        except AttributeError:
                            # Celler utan tooltip
                            key = tr.select_one("th").text.strip()

                        values = [x.text.strip() for x in tr.select("td.data-pager__page")]
                        table_data[key] = list(zip(years, values))

                    table_data = _prefix_keys(table_data, "Nycketal")
                    data.update(table_data)
                self._accounts_data = data
        return self._accounts_data

    def _clean_data(self, dict_):
        for key, value in dict_.items():
            if key in PARSERS:
                parser = PARSERS[key]
                dict_[key] = parser(value)

        return dict_

    def _get_soup(self, endpoint=None):
        url = self.url
        if endpoint:
            url += "/{}".format(endpoint)
        print("/GET {}".format(url))
        r = requests.get(url)
        r.raise_for_status()
        return BeautifulSoup(r.content, "html.parser")
