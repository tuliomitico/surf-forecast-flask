import json
import logging
from flask.json import jsonify
from flask_classful import FlaskView, route
from flask_jwt_extended import current_user,jwt_required

from . import BaseController
from ..models.beach import Beach
from ..services.forecast import Forecast
from ..utils.errors.api_error import APIError

forecast = Forecast()

class ForecastController(FlaskView, BaseController):
    route_base = "/forecast"
    trailing_slash = False
    decorators=[jwt_required()]

    @route('')
    def get_forecast_for_logged_user(self):
        try:
            beaches = Beach.objects.filter(user=current_user.id)
            result = json.loads(beaches.to_json())
            forecast_data = forecast.process_forecast_for_beaches(result)
            return jsonify(forecast_data), 200
        except Exception as e:
            logging.error(repr(e))
            return self._send_error_response(api_error=APIError(code=500,message="Something went wrong"))
