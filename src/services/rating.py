from typing import TypedDict

from ..models.beach import Beach
from ..services.forecast import Forecast

class Height(TypedDict):
    minimum: float
    maximum: float 

class WaveHeights(TypedDict):
    ankle_to_knee: Height
    waist_high: Height
    overhead_high: Height

# meters
wave_heights: WaveHeights = {
    "ankle_to_knee": {
        "minimum": 0.3,
        "maximum": 1.0
    },
    "waist_high": {
        "minimum": 1.0,
        "maximum": 2.0
    },
    "overhead_high": {
        "minimum": 2.0,
        "maximum": 2.5
    }
}

class Rating():

    def __init__(self, beach: Beach) -> None:
        self.__beach = beach

    def get_rate_for_point(self, point: dict) -> int:
        swell_direction = self.get_position_from_location(point['swell_direction'])
        wind_direction = self.get_position_from_location(point['wind_direction'])
        wind_and_wave_rating = self.get_rating_based_on_wind_and_wave_positions(swell_direction,wind_direction)
        swell_height_rating = self.get_rating_for_swell_size(point['swell_height'])
        swell_period_rating = self.get_rating_for_swell_period(point['swell_period'])
        final_rating = round((wind_and_wave_rating + swell_height_rating + swell_period_rating) / 3)
        return final_rating

    def get_rating_based_on_wind_and_wave_positions(
        self,wave_position: str,wind_position: str
    ) -> int:
        if wave_position == wind_position:
            return 1
        elif self.__is_wind_offshore(wave_position,wind_position):
            return 5
        return 3
    
    def get_rating_for_swell_period(
        self, period: int
    ) -> int:
        if (period < 7):
            return 1
        if (period < 10): 
            return 2
        if (period < 14): 
            return 4;
        return 5;
    
    def get_rating_for_swell_size(
        self,height: float
    ) -> int:
        if (height < wave_heights["ankle_to_knee"]["minimum"]):
            return 1
        if (height < wave_heights['ankle_to_knee']['maximum']): 
            return 2
        if (height < wave_heights["waist_high"]["maximum"]): 
            return 3
        return 5

    def get_position_from_location(self, coordinates: float) -> str:
        if (coordinates < 50): 
            return "N"
        if (coordinates < 120): 
            return "E"
        if (coordinates < 220): 
            return "S"
        if (coordinates < 310): 
            return "W"
        return "N"

    def __is_wind_offshore(self,wave_position: str,wind_position: str) -> bool:
        return (
            (wave_position == "N" and wind_position == "S" and self.__beach.position=="N") or
            (wave_position == "S" and wind_position == "N" and self.__beach.position=="S") or
            (wave_position == "E" and wind_position == "W" and self.__beach.position=="E") or
            (wave_position == "W" and wind_position == "E" and self.__beach.position=="W") 
            )
