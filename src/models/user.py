import json
import mongoengine as me

from ..services.auth import AuthService

def email_count(name):
    email_count = User.objects(email=name).count()
    if email_count:
        raise me.errors.ValidationError(message=f"{name} already exists", errors={"duplicated":"DUPLICATED"})

class User(me.Document):
    name = me.StringField(required=True)
    email = me.EmailField(required=True,unique=True,validation=email_count)
    password = me.StringField(required=True)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.password = AuthService.hash_password(document.password)
    
    def to_json(self, *args, **kwargs):
        result = json.loads(super().to_json(*args, **kwargs))
        result['id'] = result['_id']['$oid']
        del result['_id']
        return result

me.signals.pre_save.connect(User.pre_save, sender=User)
   