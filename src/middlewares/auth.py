from flask_jwt_extended import JWTManager

from ..models.user import User

jwt = JWTManager()

@jwt.invalid_token_loader
def my_invalid_token_callback(jwt_payload):
    if jwt_payload == 'Not enough segments':
        return dict(code = 401,error = 'jwt malformed'), 401
    if jwt_payload == 'Signature verification failed':
        return dict(code = 401, error= 'jwt signature error'), 401

@jwt.unauthorized_loader
def my_unauthorized_callback(jwt_payload: str):
    if jwt_payload == 'Missing Authorization Header':
        return dict(code=401, error='jwt must be provided'), 401

@jwt.token_verification_failed_loader
def my_token_verification_failed(jwt_payload):
    return dict(code=401, error='jwt must be provided'), 401

@jwt.user_lookup_error_loader
def my_user_lookup_error(_jwt_header,jwt_data):
    return dict(code=404,message='User not found!'),404

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    try:
        identity = jwt_data["sub"]["id"]
        user = User.objects(id=identity).first()
        return user
    except KeyError:
        return None 