"""Beach functinal tests"""
import json
from flask import Flask
from flask.testing import FlaskClient
import pytest

from src.models.beach import Beach
from src.models.user import User
from src.services.auth import AuthService


default_user = {
    "name": "John Doe",
    "email": "john@mail.com",
    "password": "1234"
}

@pytest.fixture(scope='function')
def clean_beaches(app: Flask):
  Beach.objects.delete()
  User.objects.delete()
  user = User(**default_user).save()
  with app.test_request_context():
    token = AuthService.generate_token(user.to_json())
    print(token)  
    return token

def test_create_a_beach(clean_beaches: str, client: FlaskClient):
    beaches = {
        "lat": -33.792726,
        "lng": 151.289824,
        "name": "Manly",
        "position": "E",
    }
    headers = {"Authorization": f'Bearer {clean_beaches}'}
    response = client.post('/beaches',headers=headers,json=beaches)
    assert response.status_code == 201
    assert set(beaches.items()).issubset(set(response.json.items()))

def test_throw_error(clean_beaches: str, client: FlaskClient):
    beaches = {
        "lat": "string",
        "lng": 151.289824,
        "name": "Manly",
        "position": "E",
    }
    headers = {"Authorization": f'Bearer {clean_beaches}'}
    response = client.post('/beaches',headers=headers,json=beaches)
    assert response.status_code == 422
    assert response.json['error'] == "Unprocessable Entity"
    assert response.json['message'] == "ValidationError (Beach:None) (FloatField only accepts float and integer values: ['lat'])"

@pytest.mark.skip("Should return 500 when there any error other than validation error")
def test_internal_error():
    assert True