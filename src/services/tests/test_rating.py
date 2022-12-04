"""Ratings service"""
import pytest


from ..rating import Rating
from ...models.beach import Beach

pytestmark = pytest.mark.unit

beach = {
    "lat": -33.792726,
    "lng": 151.289824,
    "name": "Manly",
    "position": "E",
}

point = {
    "swell_direction": 110,
    "swell_height": 0.1,
    "swell_period": 5,
    "time": 'test',
    "wave_direction": 110,
    "wave_height": 0.1,
    "wind_direction": 100,
    "wind_speed": 100,
}

default_rating = Rating(Beach(**beach))

# Calculate rate for a given point.
def test_poor_point():
    """Get a rating for less than 1 for a poor point"""
    rating = default_rating.get_rate_for_point(point)
    assert rating == 1

def test_ok_point():
    """Get a rating of 1 for an OK point"""
    point['swell_height'] = 0.4
    rating = default_rating.get_rate_for_point(point)
    assert rating == 1

def test_regular_point():
    """Get a rating of 3 for a point with offshore winds and a half overhead height"""
    point['swell_height'] = 0.7
    point['wind_direction'] = 250
    rating = default_rating.get_rate_for_point(point)
    assert rating == 3

def test_optimal_point():
    """Get a rating of 4 for a point with offshore winds,half overhead high swell and good interval"""
    point['swell_height'] = 0.7
    point['wind_direction'] = 250
    point['swell_period'] = 12
    rating = default_rating.get_rate_for_point(point)
    assert rating == 4

def test_optimal_point_2():
    """Get a rating of 4 for a point with offshore winds, shoulder high swell and good interval"""
    point["swell_height"] = 1.5
    point["swell_period"] = 12
    point["wind_direction"] = 250
    rating = default_rating.get_rate_for_point(point)
    assert rating == 4
    
def test_classic_day():
    """Get a rating of 5 classic day!"""
    point['swell_height'] = 2.5
    point['swell_period'] = 16
    point['wind_direction'] = 250
    rating = default_rating.get_rate_for_point(point)
    assert rating == 5
    
def test_optimal_point_3():
    """Get a rating of 4 a good condition but with crossshore winds"""
    point["swell_height"] = 2.5
    point["swell_period"] = 16
    point["wind_direction"] = 130
    rating = default_rating.get_rate_for_point(point);
    assert rating == 4
    

@pytest.mark.skip()    
def test_padrao_2():
    """Get rating based on wind and wave positions."""

def test_onshore_winds():
    """Get rating 1 for a beach with onshore winds."""
    rating = default_rating.get_rating_based_on_wind_and_wave_positions("E","E")
    assert rating == 1

def test_cross_winds():
    """Get rating 3 for a beach with cross winds."""
    rating = default_rating.get_rating_based_on_wind_and_wave_positions("E","S")
    assert rating == 3

def test_offshore_winds():
    """Get rating 5 for a beach with offshore winds."""
    rating = default_rating.get_rating_based_on_wind_and_wave_positions("E","W")
    assert rating == 5

# Get rating based on swell period
def test_rating_period_of_5():
    """Should get a rating of 1 for a period of 5 seconds"""
    rating = default_rating.get_rating_for_swell_period(5)
    assert rating == 1

def test_rating_period_of_9():
    """Should get a rating of 2 for a period of 9 seconds"""
    rating = default_rating.get_rating_for_swell_period(9)
    assert rating == 2

def test_rating_period_of_12():
    """Should get a rating of 4 for a period of 12 seconds"""
    rating = default_rating.get_rating_for_swell_period(12)
    assert rating == 4
    
def test_rating_period_of_16():
    """Should get a rating of 5 for a period of 16 seconds"""
    rating = default_rating.get_rating_for_swell_period(16)
    assert rating == 5

# Get rating based on swell height
def test_rating_swell_size_less_than_ankle_to_knee():
    """Should get a rating of 1 for less than a ankle to knee high sweel"""
    rating = default_rating.get_rating_for_swell_size(0.2)
    assert rating == 1

def test_rating_swell_size_of_ankle_to_knee():
    """Should get a rating of 2 for an ankle to knee high sweel"""
    rating = default_rating.get_rating_for_swell_size(0.6)
    assert rating == 2

def test_rating_swell_size_of_waist():
    """Should get a rating of 3 for a waist high sweel"""
    rating = default_rating.get_rating_for_swell_size(1.5)
    assert rating == 3

def test_rating_swell_size_of_overhead():
    """Should get a rating of 5 for a overhead high sweel"""
    rating = default_rating.get_rating_for_swell_size(2)
    assert rating == 5

# Get position based on points location
def test_position_east():
    """Should get the point based on the east location"""
    rating = default_rating.get_position_from_location(92)
    assert rating == "E"

def test_position_north_1():
    """Should get the point based on the north location 1"""
    rating = default_rating.get_position_from_location(360)
    assert rating == "N"

def test_position_north_2():
    """Should get the point based on the north location 2"""
    rating = default_rating.get_position_from_location(40)
    assert rating == "N"

def test_position_south():
    """Should get the point based on the south location"""
    rating = default_rating.get_position_from_location(200)
    assert rating == "S"

def test_position_west():
    """Should get the point based on the west location"""
    rating = default_rating.get_position_from_location(300)
    assert rating == "W"
 