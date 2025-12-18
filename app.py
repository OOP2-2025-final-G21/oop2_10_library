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

    # --- 貸出関連の集計 ---
    # 現在の貸出件数（返却情報がないため全件を貸出中とみなす）
    current_borrow_count = Borrow.select().count()

    # 月別貸出回数（過去12ヶ月）
    borrow_month_q = (
        Borrow
        .select(fn.strftime('%Y-%m', Borrow.borrow_date).alias('month'), fn.COUNT(Borrow.id).alias('count'))
        .group_by(fn.strftime('%Y-%m', Borrow.borrow_date))
    )
    borrow_counts = {r.month: r.count for r in borrow_month_q}

    months = []
    for i in range(11, -1, -1):
        m = now.month - i
        y = now.year
        while m <= 0:
            m += 12
            y -= 1
        months.append(f"{y:04d}-{m:02d}")

    monthly_borrows = [{"month": m, "count": borrow_counts.get(m, 0)} for m in months]

    # よく借りられている本（ランキング上位5）
    top_books_q = (
        Book
        .select(Book, fn.COUNT(Borrow.id).alias('count'))
        .join(Borrow)
        .group_by(Book.id)
        .order_by(fn.COUNT(Borrow.id).desc())
        .limit(5)
    )

    # ジャンル別の冊数（既存テンプレート用）
    genre_stats = (
        Book.select(Book.genre, fn.COUNT(Book.id).alias('count')).group_by(Book.genre)
    )

    return render_template('index.html',
                        new_members_week=new_members_week,
                        new_members_month=new_members_month,
                        new_members_three_months=new_members_three_months,
                        current_borrow_count=current_borrow_count,
                        monthly_borrows=monthly_borrows,
                        top_books=top_books_q,
                        genre_stats=genre_stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
