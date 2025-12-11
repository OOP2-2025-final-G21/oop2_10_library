from peewee import Model, ForeignKeyField, DateTimeField
from .db import db
from .user import Member
from .product import Product

class Order(Model):
    member = ForeignKeyField(Member, backref='orders')
    product = ForeignKeyField(Product, backref='orders')
    order_date = DateTimeField()

    class Meta:
        database = db
