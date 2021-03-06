"""User functional tests"""
import logging
from flask import Flask
from flask.testing import FlaskClient
import pytest

from src.models.user import User
from src.services.auth import AuthService

@pytest.fixture(scope='function')
def clean_users(app: Flask):
  User.objects.delete()
  yield 
  User.objects.delete()


def test_create_new_user_with_encrypted_password(clean_users,client: FlaskClient):
    """Should sucessfully create a new user with encrypted password"""
    new_user = {
        "name": "John Doe",
        "email": "john@mail.com",
        "password": "1234"
    }
    response = client.post('/users',json=new_user)
    assert response.status_code == 201
    assert AuthService.compare_password(new_user['password'], response.json['password'])
    assert set(new_user.keys()).issubset(set(response.json.keys()))

def test_throw_validation_error_422(client: FlaskClient):
    new_user = {
        "email": "john@mail.com",
        "password": "1234"
    }
    response = client.post('/users',json=new_user)
    assert response.status_code == 422
    assert response.json == {"code": 422,"error": "ValidationError (User:None) (Field is required: ['name'])"}
    
def test_throw_validation_error_409(clean_users,client: FlaskClient):
    new_user = {
        "name": "John Doe",
        "email": "john@mail.com",
        "password": "1234"
    }
    client.post('/users',json=new_user)
    response = client.post('/users',json=new_user)
    assert response.status_code == 409
    assert response.json == {"code": 409,"error":"ValidationError (User:None) (john@mail.com already exists(DUPLICATED: ['duplicated']): ['email'])"}

def test_authenticate_user(clean_users, client: FlaskClient):
    """Should generate a token for a valid user
    """
    new_user = {
        "name": "John Doe",
        "email": "john@mail.com",
        "password": "1234"
    }
    User(**new_user).save()
    response = client.post(
        '/users/authenticate',
        json={
            "email" : new_user['email'], "password": new_user["password"]
    })
    print(response.json)
    assert response.status_code == 200
    assert type(response.json["token"]) == str

def test_authenticate_user_unauthorized(client: FlaskClient):
    "Should return UNAUTHORIZED if the user with the given email doesn't exists"
    response = client.post('/users/authenticate',json={"email" : "some-email@mail.com", "password": "1234"})
    assert response.status_code == 401

def test_authenticate_user_unauthorized(client: FlaskClient):
    "Should return UNAUTHORIZED if the user is found, but the password doesn't match"
    new_user = {
        "name": "John Doe",
        "email": "john@mail.com",
        "password": "1234"
    }
    User(**new_user).save()
    response = client.post(
        '/users/authenticate',
        json={
            "email" : new_user['email'], "password": 'different-password'
    })
    assert response.status_code == 401