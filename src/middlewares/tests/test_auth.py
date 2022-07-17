from unittest.mock import Mock

import pytest
from flask import Flask
from flask_jwt_extended import jwt_required

from ...services.auth import AuthService

@pytest.mark.unit
def test_call_next_middleware(app: Flask):
    with app.test_request_context():
        jwt_token = AuthService.generate_token({"data":'fake'})
        with app.test_request_context('request',headers={'Authorization': f'Bearer {jwt_token}'}):
            req_fake = {"headers": {"Authorization": jwt_token}}
            res_fake = {}
            next_fake = Mock()
            auth_middleware = jwt_required(next_fake)
            assert not next_fake.called