import pytest
from allabolag.request_client import RequestsRequestClient, RotatingIPRequestClient, RequestError
from allabolag.company import Company

def test_requests_client_with_real_company():
    client = RequestsRequestClient()
    url = f"https://www.allabolag.se/5590712807"
    
    response = client.get(url)
    
    assert response.status_code == 200

def test_rotating_ip_client_with_real_company():
    client = RotatingIPRequestClient()
    url = f"https://www.allabolag.se/5590712807"
    
    response = client.get(url)
    
    assert response.status_code == 200
# ... existing code ...

def test_company_with_rotating_ip_client():
    company = Company("5590712807", RequestClient=RotatingIPRequestClient)
    assert company.data is not None
