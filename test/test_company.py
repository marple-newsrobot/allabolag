from allabolag import Company, NoSuchCompany
import pytest
import re

def test_company_raw_data():
    c = Company("559071-2807")
    assert c.raw_data["company"]["name"] == "Journalism Robotics Stockholm AB"


def test_company_clean_data():
    c = Company("559071-2807")
    sample_account = c.data["company"]["companyAccounts"][0]["accounts"][0]
    assert "code_translated" in sample_account
    assert isinstance(sample_account["amount"], float)


def test_invalid_company():
    with pytest.raises(NoSuchCompany):
        c = Company("559071-xxxx")
        c.data

