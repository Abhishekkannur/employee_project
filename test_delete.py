import pytest
from fastapi.testclient import TestClient
import main
from routers.auth import create_access_token
from datetime import timedelta
from models import *
client=TestClient(main.app)
employee_id=31
profile_id=18
def test_delete_employee_profile():
    access_token = create_access_token(username="abhishekk", user_id=15, expires_delta=timedelta(minutes=15))
    headers = {"Authorization": f"Bearer {access_token}"}

    response=client.delete(f"employee/delete_employee_profile/{profile_id}",headers=headers)
    assert response.status_code==204
    print(response.json())

def test_delete_employee():
    access_token = create_access_token(username="abhishekk", user_id=15, expires_delta=timedelta(minutes=15))
    headers = {"Authorization": f"Bearer {access_token}"}
    response=client.delete(f"/employee/delete_employee/{employee_id}",headers=headers)
    assert response.status_code== 204
    