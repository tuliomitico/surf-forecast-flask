import json

from pytest_mock import MockerFixture
from requests.exceptions import HTTPError
import pytest
import requests

from ...clients.storm_glass import ClientRequestError, StormGlass, StormGlassResponseError

pytestmark = pytest.mark.unit

def test_get_weather(test_request, mocker: MockerFixture) -> None:
    storm_glass_3_hours_fixture = json.loads(open('./tests/fixtures/stormglass_3_hours.json',mode='r').read())
    storm_glass_3_hours_normalized_fixture = json.loads(open('./tests/fixtures/stormglass_3_hours_normalized.json',mode='r').read())
    lat = -33.792726
    lng = 151.289824
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = storm_glass_3_hours_fixture
    mocker.patch('requests.get',return_value=mock_response)
    storm_glass = StormGlass(requests)
    response = storm_glass.fetch_points(lat,lng)
    assert response == storm_glass_3_hours_normalized_fixture

def test_incomplete_points(test_request, mocker: MockerFixture) -> None:
    lat = -33.792726
    lng = 151.289824
    incomplete_points = {
        "hours": [
            {
                "windDirection": {
                    "noaa": 300
                },
                "time": "2020-04-26T00:00:00+00:00"
                
            }
        ]
    }
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = incomplete_points
    mocker.patch('requests.get',return_value=mock_response)
    storm_glass = StormGlass(requests)
    response = storm_glass.fetch_points(lat,lng)
    assert response == []

def test_generic_error(test_request, mocker: MockerFixture) -> None:
    mocker.patch('requests.Response.raise_for_status',side_effect=ClientRequestError('Network Error'))
    with pytest.raises(Exception,match='Unexpected error when trying to communicate to StormGlass: Network Error'):
        lat = -33.792726
        lng = 151.289824
        storm_glass = StormGlass(requests)
        response = storm_glass.fetch_points(lat,lng)
        assert response == []

def test_rate_limit_error(test_request, mocker: MockerFixture) -> None:
    mocker.patch('requests.Response.raise_for_status',side_effect=requests.ConnectionError("Error: 429, data: errors: [Rate Limit Reached]"))
    with pytest.raises(Exception):
        lat = -33.792726
        lng = 151.289824
        storm_glass = StormGlass(requests)
        response = storm_glass.fetch_points(lat,lng)
        assert response == []