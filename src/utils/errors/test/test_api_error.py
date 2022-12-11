"""ApiError"""
import pytest

from ..api_error import APIError, ApiError 

pytestmark = pytest.mark.unit

def test_should_format_error_with_mandatory_fields():
    error = ApiError.format(APIError(**{ "code": 404, "message": 'User not found!' }))
    assert error == {
      "message": 'User not found!',
      "error": 'Not Found',
      "code": 404,
    }

def test_should_format_error_with_mandatory_fields_and_description():
    error = ApiError.format(APIError(**{
      "code": 404,
      "message": 'User not found!',
      "description": 'This error happens when there is no user created',
    }))
    assert error == {
      "message": 'User not found!',
      "error": 'Not Found',
      "code": 404,
      "description": 'This error happens when there is no user created',
    }


def test_should_format_error_with_mandatory_fields_and_description_and_documentation():
    error = ApiError.format(APIError(**{
      "code": 404,
      "message": 'User not found!',
      "description": 'This error happens when there is no user created',
      "documentation": 'https://mydocs.com/error-404',
    }))
    assert error == {
      "message": 'User not found!',
      "error": 'Not Found',
      "code": 404,
      "description": 'This error happens when there is no user created',
      "documentation": 'https://mydocs.com/error-404',
    }
  