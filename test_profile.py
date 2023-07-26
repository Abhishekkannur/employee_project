import pytest
from fastapi.testclient import TestClient
import main
from routers.auth import create_access_token
from datetime import timedelta
from models import *

client = TestClient(main.app)
employee_id=31
profile_id=23
def test_create_employee_profile_authenticated():
    access_token = create_access_token(username="abhishekk", user_id=20, expires_delta=timedelta(minutes=15))
    headers = {"Authorization": f"Bearer {access_token}"}
    employee_data = {
        "date_of_birth": "1998-02-20",
        "address": "mbl",
        "country": "India",
        "Intrests": "cricket"
        
    }
    response = client.post(f"/employee/create_profile/{employee_id}", json=employee_data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    print(response.json())

def test_create_employee_profile_not_authenticated():
    employee_data = {
         "date_of_birth": "1998-02-20",
        "address": "mbl",
        "country": "India",
        "Intrests": "cricket",
        
    }
    response = client.post(f"/employee/create_profile/{employee_id}", json=employee_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    print(response.json())

def test_get_employee_profile_by_id():
    access_token = create_access_token(username="abhishekk", user_id=20, expires_delta=timedelta(minutes=15))
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = client.get(f"/get_employee_profile_by_id/{profile_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    print(response.json())
def test_get_employee_profile_by_invalid_id():
    access_token = create_access_token(username="abhishekk", user_id=20, expires_delta=timedelta(minutes=15))
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = client.get(f"/get_employee_profile_by_id/33", headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    print(response.json())
def test_update_profile_with_valid_data():
    access_token = create_access_token(username="abhishekk", user_id=20, expires_delta=timedelta(minutes=15))
    headers = {"Authorization": f"Bearer {access_token}"}
    employee_data = {
         "date_of_birth": "1998-02-20",
        "address": "bijapur",
        "country": "India",
        "Intrests": "cricket",
        
    }
    response = client.put(f"/employee/update_employee_profile/{profile_id}", json=employee_data,headers=headers)
    assert response.status_code == status.HTTP_200_OK
    print(response.json())


