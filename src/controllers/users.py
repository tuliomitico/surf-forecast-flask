import json

from flask.json import jsonify
from flask_classful import FlaskView, route, request
from flask_jwt_extended import jwt_required, current_user
from mongoengine.errors import ValidationError

from src.utils.errors.api_error import APIError

from . import BaseController
from ..models.user import User
from ..services.auth import AuthService

class UsersController(FlaskView, BaseController):
    route_base = "/users"
    trailing_slash = False

    @route('',methods=['POST'])
    def create(self):
        try:
            data = request.get_json()
            user = User(**data)
            user.save()
            result = user.to_json()
            return result, 201
        except (ValidationError, Exception) as err:
            return self._send_create_update_error_response(err)
    
    @route('/authenticate',methods=['POST'])
    def authenticate(self):
        data = request.get_json()
        user = User.objects(email=data['email']).first()
        if not user:
            return self._send_error_response(
                APIError(code=401,message="User not found!")
            )
        if not AuthService.compare_password(data['password'], user.password):
            return self._send_error_response(
                APIError(code=401,message='Password does not match')
            )
        result = user.to_json()
        token = AuthService.generate_token(result)
        return dict(**result,token=token), 200

    @route('/me')
    @jwt_required()
    def me(self):
        if not current_user:
            return self._send_error_response(APIError(code=404),message='User not found!')
        user: User = current_user
        return user.to_json(), 200


    def get(self):
        user = User.objects.all()
        result = json.loads(user.to_json())
        for i in result:
            i['id'] = i['_id']
            del i['_id']
        return jsonify(result)
