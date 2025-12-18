from flask import Flask, render_template
from models import initialize_database
from routes import blueprints
from models.user import Member
from models.book import Book
from models.borrow import Borrow
from peewee import fn
from datetime import datetime, timedelta

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def index():
    # 現在の日時
    now = datetime.now()

    # 最近7日間に登録された会員数
    week_ago = now - timedelta(days=7)
    new_members_week = Member.select().where(Member.created_at >= week_ago).count()

    # 最近30日間に登録された会員数
    month_ago = now - timedelta(days=30)
    new_members_month = Member.select().where(Member.created_at >= month_ago).count()

    # 最近90日間に登録された会員数
    three_months_ago = now - timedelta(days=90)
    new_members_three_months = Member.select().where(Member.created_at >= three_months_ago).count()

    # Bookのジャンル別件数を取得
    genre_stats = (
        Book
        .select(Book.genre, fn.COUNT(Book.id).alias('count'))
        .group_by(Book.genre)
    )

    return render_template('index.html',
                        new_members_week=new_members_week,
                        new_members_month=new_members_month,
                        new_members_three_months=new_members_three_months)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
