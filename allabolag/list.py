import requests
from bs4 import BeautifulSoup
import json


def iter_list(base, limit=None, start_from=1):
    """Iterate a search result list

    :param base: list url fragment
    :param limit: a function to limit results, eg by date
    """
    page = start_from or 1
    has_more_results = True

    list_url = f"https://www.allabolag.se/{base}/"
    while has_more_results:
        url = f"{list_url}?page={page}"
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
