import mongoengine as me

class Beach(me.Document):
    lat = me.FloatField(required=True)
    lng = me.FloatField(required=True)
    name = me.StringField(required=True)
    position = me.StringField(required=True)
    user = me.ObjectIdField(db_field='User', required=True)

    def transform(self) -> None:
        self.id = self._id
        del self._id
        del self.__v
