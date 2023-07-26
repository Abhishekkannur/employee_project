import pytest
from fastapi.testclient import TestClient
import main
from routers.auth import create_access_token
from datetime import timedelta
from models import *
client = TestClient(main.app)
def test_create_user():
    user_data = {
        "username": "abhishekk",
        "password": "917353"
    }

    response = client.post("/auth/create_user", json=user_data)
    assert response.status_code == 200
    print(response._content)
    print(response.json())
    

def test_login_for_access_token():
    login_data = {
        "username": "abhishekk",
        "password": "917353",
        "grant_type": "password"
    }

    response = client.post("/auth/token", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    print(response.json())