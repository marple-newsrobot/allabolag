import requests
from bs4 import BeautifulSoup
from datetime import datetime
from copy import deepcopy
import re
import json
from allabolag.utils import _dl_to_dict


def iter_liquidated_companies(until):
    """Iterate the paginated list of liquidated companies ("konkurs inledd").
    The website does not allow us to fetch a given date (range). We may only
    collect the latest records.

    :param until: date of oldest liquidation.
    """
    if not isinstance(until, datetime):
        until = datetime.strptime(until, "%Y-%m-%d")
    page = 1
    has_more_results = True

    while has_more_results:
        url = "https://www.allabolag.se/lista/konkurs-inledd/6/?page={}".format(page)
        print("/GET {}".format(url))
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "html.parser")
        data = json.loads(soup.select_one(".page.search-results search")\
                              .attrs[":search-result-default"])

        if len(data) == 0:
            raise Exception(u"No results on {}".format(url))

        for item in data:
            item_data = _parse_liquidated_company_item(item)
            if item_data["Konkurs inledd"] < until:
                has_more_results = False
            else:
                yield item_data

        page += 1

def _parse_liquidated_company_item(item_dict):
    item = deepcopy(item_dict)

    # store for backward compability
    item["link"] = item_dict["linkTo"]
    item["Org.nummer"] = item_dict["orgnr"]

    for remark in item_dict["remarks"]:
        key = remark["remarkDescription"] # ie. Konkurs inledd
        item[key] = datetime.strptime(remark["remarkDate"], "%Y-%m-%d")

    return item
