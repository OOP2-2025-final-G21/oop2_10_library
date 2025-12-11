from peewee import Model, ForeignKeyField, DateTimeField
from .db import db
from .user import Member
from .book import Book

class Borrow(Model):
    member = ForeignKeyField(Member, backref='borrows')
    book = ForeignKeyField(Book, backref='borrows')
    borrow_date = DateTimeField()

    class Meta:
        database = db
