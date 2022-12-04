"""Forecas Service"""

import json
import pytest
from pytest_mock import MockerFixture

from ...clients.storm_glass import StormGlass
from ...services.forecast import Forecast, ForecastProcessingInternalError

pytestmark = pytest.mark.unit

def test_should_return_the_forecast_for_mutiple_beaches_in_the_same_hour_with_different_ratings(mocker: MockerFixture):
    mocker.patch.object(StormGlass,'fetch_points',side_effect=[[
      {
        "swellDirection": 123.41,
        "swellHeight": 0.21,
        "swellPeriod": 3.67,
        "time": '2020-04-26T00:00:00+00:00',
        "waveDirection": 232.12,
        "waveHeight": 0.46,
        "windDirection": 310.48,
        "windSpeed": 100,
      },
    ],[
      {
        "swellDirection": 64.26,
        "swellHeight": 0.15,
        "swellPeriod": 13.89,
        "time": '2020-04-26T00:00:00+00:00',
        "waveDirection": 231.38,
        "waveHeight": 2.07,
        "windDirection": 299.45,
        "windSpeed": 100,
      },
    ]])
    
    
    beaches = [
      {
        "lat": -33.792726,
        "lng": 151.289824,
        "name": 'Manly',
        "position": "E",
        "user": 'fake-id',
      },
      {
        "lat": -33.792726,
        "lng": 141.289824,
        "name": 'Dee Why',
        "position": "S",
        "user": 'fake-id',
      },
    ];
    expected_response = [
      {
        "time": '2020-04-26T00:00:00+00:00',
        "forecast": [
          {
            "lat": -33.792726,
            "lng": 151.289824,
            "name": 'Manly',
            "position": 'E',
            "rating": 2,
            "swellDirection": 123.41,
            "swellHeight": 0.21,
            "swellPeriod": 3.67,
            "time": '2020-04-26T00:00:00+00:00',
            "waveDirection": 232.12,
            "waveHeight": 0.46,
            "windDirection": 310.48,
            "windSpeed": 100,
          },
          {
            "lat": -33.792726,
            "lng": 141.289824,
            "name": 'Dee Why',
            "position": 'S',
            "rating": 3,
            "swellDirection": 64.26,
            "swellHeight": 0.15,
            "swellPeriod": 13.89,
            "time": '2020-04-26T00:00:00+00:00',
            "waveDirection": 231.38,
            "waveHeight": 2.07,
            "windDirection": 299.45,
            "windSpeed": 100,
          },
        ],
      },
    ];
    forecast = Forecast(StormGlass())
    beaches_with_rating = forecast.process_forecast_for_beaches(beaches)
    assert beaches_with_rating == expected_response

def test_should_return_forecast_for_a_list_of_beaches(mocker: MockerFixture) -> None:
    storm_glass_3_hours_normalized_fixture = json.loads(open('./tests/fixtures/stormglass_3_hours_normalized.json',mode='r').read())
    mocker.patch.object(StormGlass,'fetch_points',return_value=storm_glass_3_hours_normalized_fixture)
    beaches = [
        {
            "lat": -33.792726,
            "lng": 151.289824,
            "name": "Manly",
            "position": "E",
            "user": "some-id"
        }
    ]
    expected_response = [
    {   
        "time": "2020-04-26T00:00:00+00:00",
        "forecast":[
            {
                "lat": -33.792726,
                "lng": 151.289824,
                "name": "Manly",
                "position": "E",
                "rating": 2,
                "swellDirection": 64.26,
                "swellHeight": 0.15,
                "swellPeriod": 3.89,
                "time": "2020-04-26T00:00:00+00:00",
                "waveDirection": 231.38,
                "waveHeight": 0.47,
                "windDirection": 299.45,
                "windSpeed": 100
            }
        ]
    },
    {
        "time": "2020-04-26T01:00:00+00:00",
        "forecast": [{"lat": -33.792726,
        "lng": 151.289824,
        "name": "Manly",
        "position": "E",
        "rating": 2,
        "swellDirection": 123.41,
        "swellHeight": 0.21,
        "swellPeriod": 3.67,
        "time": "2020-04-26T01:00:00+00:00",
        "waveDirection": 232.12,
        "waveHeight": 0.46,
        "windDirection": 310.48,
        "windSpeed": 100}]
    },
    {
        "time": "2020-04-26T02:00:00+00:00",
        "forecast": [{ "lat": -33.792726,
        "lng": 151.289824,
        "name": "Manly",
        "position": "E",
        "rating": 2,
        "swellDirection": 182.56,
        "swellHeight": 0.28,
        "swellPeriod": 3.44,
        "time": "2020-04-26T02:00:00+00:00",
        "waveDirection": 232.86,
        "waveHeight": 0.46,
        "windDirection": 321.5,
        "windSpeed": 100}]
    }
]
    forecast = Forecast(StormGlass())
    beaches_with_rating = forecast.process_forecast_for_beaches(beaches)
    assert beaches_with_rating == expected_response

def test_empty_beaches():
    forecast = Forecast()
    response = forecast.process_forecast_for_beaches([])
    assert response == []

def test_internal_error(mocker: MockerFixture):
    mocker.patch.object(StormGlass,'fetch_points',side_effect=ForecastProcessingInternalError('Error fetching data'))
    beaches = [
        {
            "lat": -33.792726,
            "lng": 151.289824,
            "name": "Manly",
            "position": "E",
            "user": "some-id"
        }
    ]
    forecast = Forecast(StormGlass())
    with pytest.raises(ForecastProcessingInternalError,match='Error fetching data'):
        assert forecast.process_forecast_for_beaches(beaches)