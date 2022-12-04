import logging
from ..clients.storm_glass import StormGlass
from ..utils.errors.internal_error import InternalError

class ForecastProcessingInternalError(InternalError):
    def __init__(self, message: str) -> None:
        super().__init__(f'Unexpected error during the forecast processing: {message}')

class Forecast():
    def __init__(self, storm_glass: StormGlass = StormGlass()) -> None:
        self._storm_glass = storm_glass
    
    def process_forecast_for_beaches(self, beaches: list):
        point_with_correct_source = []
        logging.info(f"Preparing the forecast for {len(beaches)} beaches")
        try:
            self.__enriched_beach_data(beaches, point_with_correct_source)

            return self.__map_forecast_by_time(point_with_correct_source)
        except ForecastProcessingInternalError as err:
            logging.error(repr(err))
            raise ForecastProcessingInternalError(err.message)

    def __enriched_beach_data(self, beaches, point_with_correct_source: list):
        for beach in beaches:
            points = self._storm_glass.fetch_points(beach['lat'],beach['lng'])
            for point in points:
                point['lat'] = beach['lat']
                point['lng'] = beach['lng']
                point['name'] = beach['name']
                point['position'] = beach['position']
                point['rating'] = 1
            point_with_correct_source.extend(points)
    

    def __map_forecast_by_time(self, forecast: 'list[dict[str,object]]'):
        forecast_by_time = []
        for point in forecast:
            forecast_by_time.append({'time': point['time'], 'forecast': [{**point}]})
        return forecast_by_time