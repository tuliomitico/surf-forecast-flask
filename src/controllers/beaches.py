import json
import logging

from flask.json import jsonify
from flask_classful import FlaskView, route, request
from flask_jwt_extended import jwt_required, current_user
from mongoengine.errors import ValidationError

from ..models.beach import Beach

class BeachesController(FlaskView):
    route_base = "/beaches"
    trailing_slash = False
    decorators=[jwt_required()]

    @route('',methods=['POST'])
    def create(self):
        try:
            data = request.get_json()
            print(current_user)
            beach = Beach(user=current_user.id,**data)
            beach.save()
            result = json.loads(beach.to_json())
            result['id'] = result['_id']['$oid']
            result['user'] = result['User']['$oid']
            del result['User']
            del result['_id']
            return result, 201
        except (ValidationError,Exception) as e:
            if not getattr(e,'message'):
                logging.error(repr(e))
                return {"error": "Internal Error"}, 500
            return {"error": e.message}, 422
    @route('')
    def get(self):
        try:
            beach = Beach.objects.all()
            result = json.loads(beach.to_json())
            for i in result:
                i['id'] = i['_id']
                del i['_id']
            return jsonify(result)
        except (ValidationError,Exception) as e:
            if not getattr(e,'message'):
                return {"error": "Internal Error"}, 500
            return {"error": e.message}, 422
