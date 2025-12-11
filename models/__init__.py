from peewee import SqliteDatabase
from .db import db
from .user import Member
from .product import Product
from .order import Order

# モデルのリストを定義しておくと、後でまとめて登録しやすくなります
MODELS = [
    Member,
    Product,
    Order,
]

# データベースの初期化関数
def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    db.close()