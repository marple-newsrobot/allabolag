import requests
from bs4 import BeautifulSoup
import json


def iter_list(base, limit=None):
    """Iterate a search result list

    :param base: list url fragment
    :param limit: a function to limit results, eg by date
    """
    page = 1
    has_more_results = True

    while has_more_results:
        LIST_BASE = "https://www.allabolag.se/lista"
        url = f"{LIST_BASE}/{base}/?page={page}"
        print("/GET {}".format(url))
        r = requests.get(url)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "html.parser")
        data = json.loads(
            soup.select_one(".page.search-results search")
            .attrs[":search-result-default"]
        )

        if len(data) == 0:
            raise Exception(u"No results on {}".format(url))

        for item in data:
            if limit and limit(item):
                has_more_results = False
            else:
                yield item

        page += 1
