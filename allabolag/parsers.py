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


# Define parser for specific data fields
PARSERS = {
    u"Aktivitet och status - Anledning till avregistrering": text,
    u"Aktivitet och status - Anmärkning": text,
    u"Aktivitet och status - Bolaget registrerat": text,
    u"Aktivitet och status - Bolagsform": text,
    u"Aktivitet och status - F-Skatt": text,
    u"Aktivitet och status - Kommunsäte": text,
    u"Aktivitet och status - Länsäte": text,
    u"Aktivitet och status - Moms": text,
    u"Aktivitet och status - SNI-bransch": text,
    u"Aktivitet och status - SNI-kod": text,
    u"Aktivitet och status - Slutdatum för F-Skatt": text,
    u"Aktivitet och status - Startdatum för F-Skatt": text,
    u"Aktivitet och status - Startdatum för moms": text,
    u"Aktivitet och status - Status": text,
    u"Aktivitet och status - Verksamhet & ändamål": text,
    u"Aktivitet och status - Ägandeförhållande": text,
    u"Balansräkningar (tkr) - Anläggningstillgångar": date_value_list,
    u"Balansräkningar (tkr) - Avsättningar (tkr)": date_value_list,
    u"Balansräkningar (tkr) - Eget kapital": date_value_list,
    u"Balansräkningar (tkr) - Kortfristiga skulder": date_value_list,
    u"Balansräkningar (tkr) - Långfristiga skulder": date_value_list,
    u"Balansräkningar (tkr) - Obeskattade reserver": date_value_list,
    u"Balansräkningar (tkr) - Omsättningstillgångar": date_value_list,
    u"Balansräkningar (tkr) - Skulder och eget kapital": date_value_list,
    u"Balansräkningar (tkr) - Skulder, eget kapital och avsättningar": date_value_list,
    u"Balansräkningar (tkr) - Tecknat ej inbetalt kapital": date_value_list,
    u"Balansräkningar (tkr) - Tillgångar": date_value_list,
    u"Löner & utdelning (tkr) - Löner till styrelse & VD": date_value_list,
    u"Löner & utdelning (tkr) - Löner till övriga anställda": date_value_list,
    u"Löner & utdelning (tkr) - Omsättning": date_value_list,
    u"Löner & utdelning (tkr) - Sociala kostnader": date_value_list,
    u"Löner & utdelning (tkr) - Utdelning till aktieägare": date_value_list,
    u"Löner & utdelning (tkr) - Varav resultatlön till övriga anställda": date_value_list,
    u"Löner & utdelning (tkr) - Varav tantiem till styrelse & VD": date_value_list,
    u"Nycketal - Antal anställda": date_value_list,
    u"Nycketal - Bruttovinstmarginal": date_value_list,
    u"Nycketal - Du Pont-modellen": date_value_list,
    u"Nycketal - Kassalikviditet": date_value_list,
    u"Nycketal - Nettoomsättning per anställd (tkr)": date_value_list,
    u"Nycketal - Nettoomsättningförändring": date_value_list,
    u"Nycketal - Personalkostnader per anställd (tkr)": date_value_list,
    u"Nycketal - Rörelsekapital/omsättning": date_value_list,
    u"Nycketal - Rörelseresultat, EBITDA": date_value_list,
    u"Nycketal - Soliditet": date_value_list,
    u"Nycketal - Vinstmarginal": date_value_list,
    u"Resultaträkning (tkr) - Nettoomsättning": date_value_list,
    u"Resultaträkning (tkr) - Resultat efter finansnetto": date_value_list,
    u"Resultaträkning (tkr) - Rörelseresultat (EBIT)": date_value_list,
    u"Resultaträkning (tkr) - Årets resultat": date_value_list,
    u"Resultaträkning (tkr) - Övrig omsättning": date_value_list,
    u"Översikt - Anmärkning": text,
    u"Översikt - Besöksadress": text,
    u"Översikt - Bolagsform": text,
    u"Översikt - F-Skatt": text,
    u"Översikt - Län": text,
    u"Översikt - Moms": text,
    u"Översikt - Omsättning": value,
    u"Översikt - Ort": text,
    u"Översikt - Registreringsår": text,
    u"Översikt - Res. e. fin": text,
    u"Översikt - Summa tillgångar": value,
    u"Översikt - Telefon": text,
    u"Översikt - Name": text,
    u"Översikt - Årets resultat": value,
}
