import json
import logging

from flask import request
from flask.json import jsonify
from flask_classful import FlaskView, route
from flask_jwt_extended import current_user,jwt_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from . import BaseController
from ..models.beach import Beach
from ..services.forecast import Forecast
from ..utils.errors.api_error import APIError, ApiError

forecast = Forecast()

limiter = Limiter(key_func=get_remote_address)

def error_message(e):
    return jsonify(ApiError.format(APIError(**{"code":429,"message": "Too many requests to /forecast endpoint"}))),429
class ForecastController(FlaskView, BaseController):
    route_base = "/forecast"
    trailing_slash = False
    decorators=[
        jwt_required(),
        limiter.limit('10/day')
    ]

    @route('')
    def get_forecast_for_logged_user(self):
        try:
            order_by, order_field = request.args.get('orderBy'), request.args.get('orderField')
            beaches = Beach.objects.filter(user=current_user.id)
            result = json.loads(beaches.to_json())
            if order_by and order_field:
                forecast_data = forecast.process_forecast_for_beaches(result,order_by,order_field)
            forecast_data = forecast.process_forecast_for_beaches(result)
            return jsonify(forecast_data), 200
        except Exception as e:
            logging.error(repr(e))
            return self._send_error_response(api_error=APIError(code=500,message="Something went wrong"))
