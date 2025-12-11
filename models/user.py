from peewee import Model, CharField, IntegerField
from .db import db

class Member(Model):
    name = CharField()
    age = IntegerField()
    email = CharField()

    class Meta:
        database = db