from peewee import Model, CharField, IntegerField
from .db import db

class Book(Model):
    title = CharField()               # 本のタイトル
    author = CharField()              # 著者名
    published_year = IntegerField()   # 発行年
    genre = CharField()               # ジャンル

    class Meta:
        database = db

    def __str__(self):
        return f"{self.title} ({self.author})"
