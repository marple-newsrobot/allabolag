import pytest
from allabolag.request_client import RequestsRequestClient, AWSGatewayRequestClient
from allabolag.company import Company
from allabolag.liquidated_companies import iter_liquidated_companies

ip_rot_request_client = AWSGatewayRequestClient()

def test_requests_client_with_real_company():
    client = RequestsRequestClient()
    url = f"https://www.allabolag.se/5590712807"
    
    response = client.get(url)
    
    assert response.status_code == 200

def test_rotating_ip_client_with_real_company():
    url = f"https://www.allabolag.se/5590712807"
    
    response = ip_rot_request_client.get(url)
    
    assert response.status_code == 200
# ... existing code ...

def test_company_with_rotating_ip_client():
    company = Company("559071-2807", request_client=ip_rot_request_client)
    assert company.data is not None

def test_iter_liquidated_companies_with_rotating_ip_client():
    for c in iter_liquidated_companies("1900-01-01", request_client=ip_rot_request_client):
        assert isinstance(c, dict)
        assert "orgnr" in c
        break


