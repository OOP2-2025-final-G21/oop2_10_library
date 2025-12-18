from peewee import Model, CharField, IntegerField, DateTimeField
from datetime import datetime
from .db import db

class Member(Model):
    name = CharField()
    age = IntegerField()
    email = CharField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db