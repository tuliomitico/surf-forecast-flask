from flask_jwt_extended import JWTManager

from ..models.user import User

jwt = JWTManager()

@jwt.invalid_token_loader
def my_invalid_token_callback(jwt_payload):
    if jwt_payload == 'Not enough segments':
        return dict(code = 401,error = 'jwt malformed'), 401

@jwt.unauthorized_loader
def my_unauthorized_callback(jwt_payload: str):
    if jwt_payload == 'Missing Authorization Header':
        return dict(code=401, error='jwt must be provided'), 401

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]['id']
    return User.objects(id=identity).first()