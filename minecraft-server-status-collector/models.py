from mongoengine import *


class Query(Document):
    timestamp = DateTimeField(required=True)
    address = StringField(required=True)
    latency = FloatField()
    version = StringField()
    description = StringField()
    players_count = IntField()
    players_max = IntField()
    players = ListField(UUIDField())
    mods = ListField(StringField())
