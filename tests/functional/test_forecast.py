"""Beach forecast functional tests
"""
import json
import pytest
from flask import Flask
from flask.testing import FlaskClient
from requests_mock.mocker import Mocker

from src.models.beach import Beach
from src.models.user import User
from src.services.auth import AuthService
from src.services.forecast import ForecastProcessingInternalError

@pytest.fixture(scope='function')
def clean_beaches(app: Flask):
  default_user = {
    "name": "John Doe",
    "email": "john@mail.com",
    "password": "1234"
  }  
  Beach.objects.delete()
  User.objects.delete()
  user = User(**default_user).save()
  data = {
        "lat": -33.792726,
        "lng": 151.289824,
        "name": "Manly",
        "position": "E",
        "user": user.id
  }
  default_beach = Beach(**data)
  default_beach.save()
  with app.test_request_context():
    token = AuthService.generate_token(user.to_json())
    return token

def test_forecast_few_times(clean_beaches: str,client: FlaskClient, requests_mock: Mocker):
    """Should return a forecast with a just few times"""
    api_forecast_response_1_beach_fixture = json.loads(open('./tests/fixtures/api_forecast_response_1_beach.json',mode='r').read())
    storm_glass_3_hours_fixture = json.loads(open('./tests/fixtures/stormglass_3_hours.json',mode='r').read())
    headers = {"Authorization": f"Bearer {clean_beaches}"}
    requests_mock.get(
        'https://api.stormglass.io/v2/weather/point?params=swellDirection,swellHeight,swellPeriod,waveDirection,waveHeight,windDirection,windSpeed&source=noaa&lat=-33.792726&lng=151.289824',
        status_code=200,
        json=storm_glass_3_hours_fixture,
    )
    rv = client.get('/forecast',headers=headers)
    data, status = rv.json, rv.status_code
    assert status == 200
    assert data == api_forecast_response_1_beach_fixture

def test_forecast_status_500(clean_beaches: str,client: FlaskClient, requests_mock: Mocker):
    """Should return 500 if something goes wrong during the processing"""
    headers = {"Authorization": f"Bearer {clean_beaches}"}
    requests_mock.get(
        'https://api.stormglass.io/v2/weather/point?params=swellDirection,swellHeight,swellPeriod,waveDirection,waveHeight,windDirection,windSpeed&source=noaa&lat=-33.792726&lng=151.289824',
        exc=ForecastProcessingInternalError,
    )
    rv = client.get('/forecast',headers=headers)
    status = rv.status_code
    assert status == 500
