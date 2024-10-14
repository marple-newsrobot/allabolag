from datetime import datetime
from copy import deepcopy
from allabolag.list import iter_list
from allabolag.request_client import RequestsRequestClient

def iter_liquidated_companies(until, request_client=RequestsRequestClient()):
    """Iterate the paginated list of liquidated companies ("konkurs inledd").
    The website does not allow us to fetch a given date (range). We may only
    collect the latest records.

    :param until: date of oldest liquidation.
    """
    raise NotImplementedError("Not working after October 2024")

