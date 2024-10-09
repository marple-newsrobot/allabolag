
from bs4 import BeautifulSoup
import re
from allabolag.utils import _dl_to_dict, _table_to_dict, _prefix_keys
from allabolag.parsers import PARSERS
from allabolag.request_client import RequestsRequestClient, RequestError
import os
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "WARNING"))
logger = logging.getLogger(__name__)


class NoSuchCompany(Exception):
    """Raised when trying to access a copmany that doesn't exist"""
    pass

default_request_client = RequestsRequestClient()

class Company():
    """Represents a single company.

    Usage:
        c = Company("559006-6642")
        print(c.data) # get all cleaned data
        print(c.raw_data) # get all uncleaned data
    """
    def __init__(self, company_code, request_client=default_request_client):
        self.company_code = company_code
        self.request_client = request_client
        self.url = f"https://www.allabolag.se/{company_code.replace('-', '')}"
        self._data = {}
        self._overview_data = {}
        self._activity_data = {}
        self._accounts_data = {}
        self._cache = {}

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
                data["account_figures_year"] = account_fig_summary_soup \
                    .select_one("h2").text.strip()
                account_fig_table = account_fig_summary_soup.select_one("table")
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
                data[u"Verksamhet & ändamål"] = verksamhet_header \
                    .parent.find_next_sibling().text.strip()

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
    def remarks(self):
        """Get a list of remarks"""
        s = self._get_soup()
        ul = s.find("ul", {"class": "remarks"})
        if not ul:
            return []
        lis = ul.find_all("li")
        return [li.text.strip() for li in lis]

    @property
    def liquidated(self):
        """Check if company is liquidated"""
        konkurs = [r for r in self.remarks if r.startswith("Konkurs")]
        likvidation = [r for r in self.remarks if r.startswith("Likvidation")]
        return True if len(konkurs) or len(likvidation) else False

    @property
    def accounts_data(self):
        """Collect data from "Bokslut & nyckeltal" """
        if self._accounts_data == {}:
            def _parse_tables(div):
                data_in_tables = {}
                for table in accounting_div.select("table"):
                    table_caption = table \
                        .select_one("thead th.company-table__pager-button-cell").text.strip()
                    if table_caption != u"Nyckeltal":
                        table_data = _table_to_dict(table)
                        table_data = _prefix_keys(table_data, table_caption)
                        data_in_tables.update(table_data)
                    else:
                        # Nyckeltal behöver egen parsing
                        # Hack Nyckeltalstabellen saknar år,
                        # därför tar vi dem från föregående år
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
                        data_in_tables.update(table_data)
                return data_in_tables
            data = {}
            s = self._get_soup("bokslut")
            # Get the h2 with text "Bolagets redovisning"
            
            accounting_heading = s.find("h2", text="Bolagets redovisning")
            if accounting_heading:
                accounting_div = accounting_heading.find_parent("div", class_="box--document")
                data.update(_parse_tables(accounting_div))

            koncern_heading = s.find("h2", text="Koncernredovisning")
            if koncern_heading:
                koncern_div = koncern_heading.find_parent("div", class_="box--document")
                data["Koncernredovisning"] = _parse_tables(koncern_div)

            self._accounts_data = data
        return self._accounts_data

    def _clean_data(self, dict_):
        for key, value in dict_.items():
            if key in PARSERS:
                parser = PARSERS[key]
                dict_[key] = parser(value)

        return dict_

    def _get_soup(self, endpoint=None):
        cache_key = endpoint
        if not cache_key:
            cache_key = "INDEX"
        if cache_key in self._cache:
            return self._cache[cache_key]
        url = self.url
        if endpoint:
            url += "/{}".format(endpoint)
        logger.info("/GET {}".format(url))
        try:
            r = self.request_client.get(url)
        except RequestError as e:
            if e.status_code == 404:
                raise NoSuchCompany(f"Company {self.company_code} not found")
            raise e
        soup = BeautifulSoup(r.content, "html.parser")
        self._cache[cache_key] = soup
        return soup
