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


def test_invalid_company():
    with pytest.raises(NoSuchCompany):
        c = Company("559071-xxxx")
        c.data


def test_liquidated():
    c = Company("5569867632")
    assert c.liquidated
