# encoding: utf-8
from allabolag import Company

def test_company():
    c = Company("559071-2807")
    data = c.data
    assert(isinstance(data, dict))
