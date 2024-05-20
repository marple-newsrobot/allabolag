import requests
from bs4 import BeautifulSoup
import json
import os
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "WARNING"))
logger = logging.getLogger(__name__)


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
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        logger.info("/GET {}".format(url))
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "html.parser")
        data = json.loads(
            soup.select_one(".page.search-results search")
            .attrs[":search-result-default"]
        )

        if len(data) == 0:
            has_more_results = False

        for item in data:
            if limit and limit(item):
                has_more_results = False
            else:
                yield item

        page += 1
