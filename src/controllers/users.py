import json

from flask.json import jsonify
from flask_classful import FlaskView, route, request
from mongoengine.errors import ValidationError

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
            return jsonify(code=401,error="User not found!"), 401
        if not AuthService.compare_password(data['password'], user.password):
            return jsonify(code=401,error='Password does not match'), 401
        result = user.to_json()
        token = AuthService.generate_token(result)
        return dict(**result,token=token), 200

    def get(self):
        user = User.objects.all()
        result = json.loads(user.to_json())
        for i in result:
            i['id'] = i['_id']
            del i['_id']
        return jsonify(result)
