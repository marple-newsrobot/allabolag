import requests
from bs4 import BeautifulSoup
from datetime import datetime
from allabolag.utils import _dl_to_dict
import re



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
        for item in soup.select(".search-results__item"):
            item_data = _parse_liquidated_company_item(item)

            if item_data["Konkurs inledd"] < until:
                has_more_results = False
            else:
                yield item_data

        page += 1

def _parse_liquidated_company_item(item_soup):
    item = {}

    a_tag = item_soup.select_one("a")
    item["link"] = a_tag["href"]
    item["Namn"] = a_tag.text.strip()

    date_str = re.search(r"Konkurs inledd (\d{4}-\d{2}-\d{2})", item_soup.text).group(1)
    item["Konkurs inledd"] = datetime.strptime(date_str, "%Y-%m-%d")

    # org nr & branch
    details = _dl_to_dict(item_soup.select_one(".search-results__item__details"))
    item.update(details)

    return item
