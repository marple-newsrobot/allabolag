from datetime import datetime


def value(s):
    """Parse float
    """
    if s is None or s == "-" or s == "":
        return None
    s = s.replace(",", ".").replace(" ", "").replace(" ", "")
    if s.endswith("%"):
        s = s.replace("%", "")
        return float(s) / 100.0
    else:
        return float(s)

    raise Exception(u"Unable to parse value from '{}'".format(s))


def date(s):
    """Parse datetime"""
    return datetime.strptime(s, "%Y-%m-%d")


def date_value(list_):
    """Parse [YEAR, VALUE] pair.

    date_value("2018-02", 25%) => [datetime(2018,2,1), 0.25]
    """
    return [
        # datetime.strptime(l[0], "%Y-%m"),
        list_[0],
        value(list_[1]),
    ]


def date_value_list(ll):
    return [date_value(list_) for list_ in ll]


def text(s):
    if s.endswith(u"Läs mer"):
        s = s.replace(u"Läs mer", "").strip()
    return s

