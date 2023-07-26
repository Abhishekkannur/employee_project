import pytest
from fastapi.testclient import TestClient
import main
from routers.auth import create_access_token
from datetime import timedelta
from models import *

client = TestClient(main.app)
test_user = Register(username="testuser", password="testpassword")
access_token = create_access_token(username=test_user.username, user_id=test_user.id, expires_delta=timedelta(minutes=15))
    
headers = {"Authorization": f"Bearer {access_token}"}

employee_id=31


def test_read_all_employees():
    response = client.get("/get_employee")
    assert response.status_code == status.HTTP_200_OK
    print(response.json())

def test_create_employee_authenticated():
    access_token = create_access_token(username="abhishekk", user_id=20, expires_delta=timedelta(minutes=15))
    headers = {"Authorization": f"Bearer {access_token}"}
    employee_data = {
        "firstname": "Mohan",
        "lastname": "Kannur",
        "email": "mohankannur@gmail.com",
        "user_id":20
    }
    response = client.post("/employee/create_employee", json=employee_data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    print(response.json())
def test_create_employee_with_invalid_data():
    access_token = create_access_token(username="abhishekk", user_id=20, expires_delta=timedelta(minutes=15))
    headers = {"Authorization": f"Bearer {access_token}"}
    employee_data = {
        "firstname": "Mohan",
        "lastname": "Kannur",
        "email": "mohankannur@gmailcom",
        "user_id":20
    }
    response = client.post("/employee/create_employee", json=employee_data, headers=headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    print(response.json())
def test_get_employee_by_id():
    access_token = create_access_token(username="abhishekk", user_id=20, expires_delta=timedelta(minutes=15))
    if access_token is None:
        # The user with the given username and user_id does not exist, skip the test
        return
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"/get_employee_by_id/{employee_id}",headers=headers)
    assert response.status_code == status.HTTP_200_OK
    print(response.json())
def test_get_employee_by_invalid_id():
    access_token = create_access_token(username="abhishekk", user_id=20, expires_delta=timedelta(minutes=15))
    if access_token is None:
        # The user with the given username and user_id does not exist, skip the test
        return
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"/get_employee_by_id/5",headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    print(response.json())

def test_update_employee():
    access_token = create_access_token(username="abhishekk", user_id=20, expires_delta=timedelta(minutes=15))
    if access_token is None:
        # The user with the given username and user_id does not exist, skip the test
        return
    headers = {"Authorization": f"Bearer {access_token}"}
    
    employee_data = {
        "firstname": "Abhishek",
        "lastname": "k",
        "email": "abhishek@gmail.com",
        "user_id":20
    }
    response = client.put(f"/employee/update_employee/{employee_id}", json=employee_data,headers=headers)
    assert response.status_code == status.HTTP_200_OK
    print(response.json())
def test_update_employee_with_invalid_data():
    access_token = create_access_token(username="abhishekk", user_id=20, expires_delta=timedelta(minutes=15))
    if access_token is None:
        # The user with the given username and user_id does not exist, skip the test
        return
    headers = {"Authorization": f"Bearer {access_token}"}
    
    employee_data = {
        "firstname": "Abhishek",
        "lastname": "k",
        "email": "abhishekgmail.com",
        "user_id":20
    }
    response = client.put(f"/employee/update_employee/{employee_id}", json=employee_data,headers=headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    print(response.json())






