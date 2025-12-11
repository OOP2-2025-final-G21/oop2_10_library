from peewee import *
from .base import BaseModel   # サンプルと同じ構成の場合は必要

class Book(BaseModel):
    title = CharField()               # 本のタイトル
    author = CharField()              # 著者名
    published_year = IntegerField()   # 発行年
    genre = CharField()               # ジャンル

    def __str__(self):
        return f"{self.title} ({self.author})"
