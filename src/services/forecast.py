import logging

from ..clients.storm_glass import StormGlass
from ..models.beach import Beach
from ..services.rating import Rating
from ..utils.errors.internal_error import InternalError

class ForecastProcessingInternalError(InternalError):
    def __init__(self, message: str) -> None:
        super().__init__(f'Unexpected error during the forecast processing: {message}')

class Forecast():
    def __init__(self, storm_glass: StormGlass = StormGlass(), rating_service: Rating = Rating) -> None:
        self._storm_glass = storm_glass
        self._rating_service = rating_service
    
    def process_forecast_for_beaches(self, beaches: list):
        point_with_correct_source = []
        logging.info(f"Preparing the forecast for {len(beaches)} beaches")
        try:
            self.__enriched_beach_data(beaches, point_with_correct_source,rating=self._rating_service)

            return self.__map_forecast_by_time(point_with_correct_source)
        except ForecastProcessingInternalError as err:
            logging.error(repr(err))
            raise ForecastProcessingInternalError(err.message)

    def __enriched_beach_data(self, beaches, point_with_correct_source: list, rating: Rating):
        for beach in beaches:
            try:
                del beach['_id']
                del beach['User']
            except:
                pass
            rating = self._rating_service(Beach(**beach))
            points = self._storm_glass.fetch_points(beach['lat'],beach['lng'])
            for point in points:
                point['lat'] = beach['lat']
                point['lng'] = beach['lng']
                point['name'] = beach['name']
                point['position'] = beach['position']
                point['rating'] = rating.get_rate_for_point(point)
            point_with_correct_source.extend(points)
    

    def __map_forecast_by_time(self, forecast: 'list[dict[str,object]]'):
        forecast_by_time = []
        for point in forecast:
            time_point = [i['time'] for i in forecast_by_time if i['time'] == point['time']] 
            print(time_point)
            if time_point:
                [forecast_by_time_2['forecast'].append(point) for forecast_by_time_2 in forecast_by_time]
            else: 
                forecast_by_time.append({'time': point['time'], 'forecast': [{**point}]})
        return forecast_by_time