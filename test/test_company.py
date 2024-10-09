from allabolag import Company, NoSuchCompany
import pytest


def test_company():
    c = Company("559071-2807")
    data = c.data
    assert(isinstance(data, dict))
    assert data["Översikt - Namn"] == "Journalism Robotics Stockholm AB"

    c = Company("5590712807")
    data = c.data
    assert(isinstance(data, dict))
    assert data["Översikt - Namn"] == "Journalism Robotics Stockholm AB"

def test_koncern_company():
    # https://www.allabolag.se/5567074199/
    c = Company("556707-4199")
    c.data
    assert "Koncernredovisning" in c.data


def test_invalid_company():
    with pytest.raises(NoSuchCompany):
        c = Company("559071-xxxx")
        c.data


#def test_liquidated():
#    c = Company("556986-7632")
#    assert c.liquidated
