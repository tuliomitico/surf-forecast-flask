import requests

from ..utils.errors.internal_error import InternalError
from ..utils import request as HTTPUtil
from ..config import Config

storm_glass_resource_config = Config()

class ClientRequestError(InternalError):
    def __init__(self, message: str) -> None:
       internal_message = 'Unexpected error when trying to communicate to StormGlass'
       super().__init__(f'{internal_message}: {message}')

class StormGlassResponseError(InternalError):
    def __init__(self, message: str) -> None:
       internal_message = 'Unexpected error returned by the StormGlass service'
       super().__init__(f'{internal_message}: {message}')

class StormGlass():
    storm_glass_api_params = "swellDirection,swellHeight,swellPeriod,waveDirection,waveHeight,windDirection,windSpeed"
    storm_glass_api_source = "noaa"
    def __init__(self, request = HTTPUtil.Request()) -> None:
        self.request = request

    def fetch_points(self, lat: float, lng: float):
        try:
            headers = {'Authorization': storm_glass_resource_config.API_TOKEN}
            response = self.request.get(
                f'{storm_glass_resource_config.API_URL}weather/point?params={self.storm_glass_api_params}&source={self.storm_glass_api_source}&lat={lat}&lng={lng}',
                headers=headers
            )
            return self.__normalize_response(response.json())
        except ClientRequestError as err:
            raise ClientRequestError(err.message)
        except requests.ConnectionError as err:
            raise StormGlassResponseError(f'Error: {err.response} Code: {429}')
        except Exception as err:
            raise Exception(str(err))

    def __normalize_response(self, points: dict):
        result = filter(self.__is_valid_point, points['hours'])
        l = list()
        for x in result:
            l.append({
                "swellDirection": x['swellDirection'][self.storm_glass_api_source],
                "swellHeight": x['swellHeight'][self.storm_glass_api_source],
                "swellPeriod": x['swellPeriod'][self.storm_glass_api_source],
                "waveDirection": x['waveDirection'][self.storm_glass_api_source],
                "waveHeight": x['waveHeight'][self.storm_glass_api_source],
                "windDirection": x['windDirection'][self.storm_glass_api_source],
                "windSpeed": x['windSpeed'][self.storm_glass_api_source],
                "time": x['time']
            })
        return l
    
    def __is_valid_point(self, points: dict) -> bool:
        points.setdefault('swellDirection',{'noaa': False})
        return bool(points['time'] and 
        points['swellDirection'][self.storm_glass_api_source] and
        points['swellHeight'][self.storm_glass_api_source] and 
        points['swellPeriod'][self.storm_glass_api_source] and 
        points['waveDirection'][self.storm_glass_api_source] and 
        points['waveHeight'][self.storm_glass_api_source] and
        points['windDirection'][self.storm_glass_api_source] and
        points['windSpeed'][self.storm_glass_api_source])