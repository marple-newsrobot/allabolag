from allabolag.request_client import RequestsRequestClient
from bs4 import BeautifulSoup
import json
import os
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "WARNING"))
logger = logging.getLogger(__name__)

default_request_client = RequestsRequestClient()

def iter_list(base, limit=None, start_from=1, request_client=default_request_client):
    """Iterate a search result list

    :param base: list url fragment
    :param limit: a function to limit results, eg by date
    """
    raise NotImplementedError("Not working after October 2024")