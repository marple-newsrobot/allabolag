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
    if not isinstance(until, datetime):
        until = datetime.strptime(until, "%Y-%m-%d")

    for item in iter_list(
        "lista/konkurs-inledd/6",
        lambda x: _parse_liquidated_company_item(x)["Konkurs inledd"] < until,
        request_client=request_client
    ):
        yield _parse_liquidated_company_item(item)


def _parse_liquidated_company_item(item_dict):
    item = deepcopy(item_dict)

    # store for backward compability
    item["link"] = item_dict["linkTo"]
    item["Org.nummer"] = item_dict["orgnr"]

    for remark in item_dict["remarks"]:
        key = remark["remarkDescription"]  # ie. Konkurs inledd
        if remark["remarkDate"] is not None:
            item[key] = datetime.strptime(remark["remarkDate"], "%Y-%m-%d")
        # TODO: Handle other remarks such as:
        # 'remarkCode': 'SHV',
        # 'remarkDescription': 'Svensk Handel Varningslistan med produktnamn: registersök.',
        # 'remarkDate': None,

    return item
