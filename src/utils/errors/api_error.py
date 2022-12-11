from dataclasses import dataclass, field
from http import HTTPStatus
from numbers import Number
from typing import Union
import http.client

@dataclass
class APIError():
    message: str
    code: Number
    code_as_string: Union[str,None] = field(default=None)
    description: Union[str,None] = field(default=None)
    documentation: Union[str,None] = field(default=None)

@dataclass
class APIErrorResponse(APIError):
    error: str = field(default_factory=str)

class ApiError():
    @staticmethod
    def format(error: APIError) -> APIErrorResponse:
        errors = {
                "message": error.message,
                "code": error.code,
                "error": error.code_as_string if error.code_as_string else http.client.responses[error.code],
        }
        if error.description:
            errors['description'] = error.description
            
        if error.documentation:
            errors['documentation'] = error.documentation
            
        return errors
