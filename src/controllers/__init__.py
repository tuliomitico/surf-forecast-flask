from __future__ import annotations
from abc import ABC
import logging

from mongoengine.errors import ValidationError, NotUniqueError

from ..utils.errors.api_error import APIError, ApiError

class BaseController(ABC):
    def _send_create_update_error_response(self, error: NotUniqueError | ValidationError | Exception):
        if isinstance(error,ValidationError):
            client_errors = self.__handle_client_errors(error)
            return ApiError.format(APIError(code=client_errors[0]['code'],message=client_errors[0]['error'])), client_errors[1] 
        logging.info(repr(error))
        return ApiError.format(APIError(**{"code": 500, "message": "Something went wrong!"})), 500

    def __handle_client_errors(self,error: ValidationError):
        if "DUPLICATED" in str(error.errors.values()):
            return {"code":409, "error": error.message}, 409 
        return {"code": 422,"error": error.message}, 422

    def _send_error_response(self, api_error: APIError):
        return ApiError.format(api_error), api_error.code
