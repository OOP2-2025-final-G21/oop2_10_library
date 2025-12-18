from peewee import ForeignKeyField, DateTimeField, fn
from .db import db
from .user import Member
from .book import Book # Bookモデルをインポート
import datetime

class Borrow(db.Model):
    user = ForeignKeyField(Member, backref='borrows') # 誰が
    book = ForeignKeyField(Book, backref='borrows') # 何を
    order_date = DateTimeField(default=datetime.datetime.now) # いつ
    return_date = DateTimeField(null=True) # 返却日（Noneなら未返却）

    class Meta:
        database = db


def total_borrows():
    """合計貸出回数を返す（Borrow レコードの件数）"""
    return Borrow.select().count()


def current_borrowed_count():
    """現在貸出中（返却日が未設定）の貸出件数を返す"""
    return Borrow.select().where(Borrow.return_date.is_null()).count()


def monthly_borrow_counts():
    """月ごとの貸出件数を ("YYYY-MM", count) のリストで返す"""
    q = (Borrow
         .select(fn.strftime('%Y-%m', Borrow.order_date).alias('month'),
                 fn.COUNT(Borrow.id).alias('count'))
         .group_by(fn.strftime('%Y-%m', Borrow.order_date))
         .order_by(fn.strftime('%Y-%m', Borrow.order_date)))
    return [(r.month, r.count) for r in q]


def top_borrowed_books(limit=5):
    """貸出回数の多い本の上位を返す。リスト要素は dict(title, count)。"""
    q = (Book
         .select(Book, fn.COUNT(Borrow.id).alias('borrow_count'))
         .join(Borrow, on=(Borrow.book == Book.id))
         .group_by(Book.id)
         .order_by(fn.COUNT(Borrow.id).desc())
         .limit(limit))
    return [{'title': b.title, 'count': b.borrow_count} for b in q]