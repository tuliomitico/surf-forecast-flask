import json
import logging
from flask.json import jsonify
from flask_classful import FlaskView, route
from flask_jwt_extended import current_user,jwt_required

from ..models.beach import Beach
from ..services.forecast import Forecast

forecast = Forecast()

class ForecastController(FlaskView):
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
            return {"error" : str(e)},500
