
def _dl_to_dict(dl):
    """
    """
    d = {}
    for dt in dl.select("dt"):
        key = dt.text.strip()
        # Assumption that the value is the next sibling
        # this is not always a dd tag (sometimes li tag for example)
        value = dt.find_next_sibling().text.strip()
        d[key] = value
    return d


def _prefix_keys(old_dict, prefix):
    """Adds a prefix to all keys in a dict"""
    new_dict = {}
    for key, value in old_dict.items():
        new_key = u"{} - {}".format(prefix, key)
        new_dict[new_key] = old_dict[key]
    return new_dict


def _table_to_dict(table):
    data = {}
    years = [x.text.strip() for x in table.select("thead th.data-pager__page")]
    for tr in table.select("tbody tr"):
        try:
            key = tr.select_one("th").text.strip()
        except Exception:
            continue
        values = [x.text.strip() for x in tr.select("td.data-pager__page")]
        data[key] = list(zip(years, values))
    return data
