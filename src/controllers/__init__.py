from __future__ import annotations
from abc import ABC

from mongoengine.errors import ValidationError, NotUniqueError

class BaseController(ABC):
    def _send_create_update_error_response(self, error: NotUniqueError | ValidationError | Exception):
        if isinstance(error,ValidationError):
            client_errors = self.__handle_client_errors(error)
            return client_errors
        return {"code": 500, "error": "Something went wrong!: {}".format(str(error))}, 500

    def __handle_client_errors(self,error: ValidationError):
        if "DUPLICATED" in str(error.errors.values()):
            return {"code":409, "error": error.message}, 409 
        return {"code": 422,"error": error.message}, 422

