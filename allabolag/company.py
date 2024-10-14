
from copy import deepcopy
from bs4 import BeautifulSoup
from allabolag import parsers
from allabolag.request_client import RequestsRequestClient, RequestError
import os
import logging
import json

logging.basicConfig(level=os.environ.get("LOGLEVEL", "WARNING"))
logger = logging.getLogger(__name__)


class NoSuchCompany(Exception):
    """Raised when trying to access a copmany that doesn't exist"""
    pass

default_request_client = RequestsRequestClient()

SECTIONS = [
    "Översikt",
    "Bokslut",
    "Nyckeltal",
    "Befattningar",
    "Organisation",
    "Händelser",
    "Varumärken",
]

NOT_IMPLEMENTED_SECTIONS = [
    "Befattningar",
    "Organisation",
    "Händelser",
    "Varumärken",
    "Rapporter",
]

BASE_URL = "https://www.allabolag.se"

class Company():
    """Represents a single company.

    Usage:
        c = Company("559006-6642")
        print(c.raw_data) # get unprocessed data
        print(c.data) # get data with translated accounting codes and parsed amounts
    """
    def __init__(self, company_code, request_client=default_request_client):
        self.company_code = company_code
        self.request_client = request_client
        self.url = f"{BASE_URL}/{company_code.replace('-', '')}"
        self._cache = {}

    @property
    def raw_data(self):
        """Get data from all sections
        """
        data = {}
        page_data = self.page_data

        props_to_keep = [
            "company",
            "trademarks",
        ]
        for prop in props_to_keep:
            data[prop] = page_data["props"]["pageProps"][prop]

        return data

    @property
    def data(self):
        cleaned_data = deepcopy(self.raw_data)
        translations = self.page_data["props"]["i18n"]["initialStore"]["sv"]
        # Translate accounting KPIs
        for yearly_account in cleaned_data["company"]["companyAccounts"] + cleaned_data["company"]["corporateAccounts"]:
            for account in yearly_account["accounts"]:
                account["amount"] = parsers.value(account["amount"])
                account["code_translated"] = translations["common"]["AccountingFigures"]["figures"]["SE"].get(account["code"])

        return cleaned_data
    
    
    @property
    def page_data(self):
        data_script_tag = self.start_soup.select_one("script#__NEXT_DATA__")
        return json.loads(data_script_tag.string)

    def _get_section_url(self, section):
        if section == "Översikt":
            return self.url
        else:
            return BASE_URL + self.start_soup.find('a', text=section).attrs['href']


    @property
    def start_soup(self):
        if not hasattr(self, '_start_soup'):
            self._start_soup = self._get_soup(self.url)
        return self._start_soup


    @property
    def remarks(self):
        """Get a list of remarks"""
        raise NotImplementedError("Needs to be updated for new site")

    @property
    def liquidated(self):
        """Check if company is liquidated"""
        raise NotImplementedError("Needs to be updated for new site")

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
