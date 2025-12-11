from peewee import SqliteDatabase
from .db import db

from .user import Member
from .book import Book
from .borrow import Borrow

# モデルのリストを定義しておくと、後でまとめて登録しやすくなります
MODELS = [
    Member,
    Book,
    Borrow,
]

# データベースの初期化関数
def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    db.close()