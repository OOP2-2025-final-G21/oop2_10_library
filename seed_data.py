import os
import sys
from datetime import datetime, timedelta
import random

# スクリプトをプロジェクトルートから実行することを想定
# (VS Code のターミナルで project root に移動して実行してください)
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from models import initialize_database
try:
    from models import Book, Member, Borrow
except Exception as e:
    print("models のインポートに失敗しました:", e)
    raise

def ensure_int(v):
    try:
        return int(v) if v is not None and v != '' else None
    except Exception:
        return None

SAMPLE_BOOKS = [
    {"title": "Python入門", "author": "山田太郎", "published_year": 2018, "genre": "プログラミング"},
    {"title": "Effective Java", "author": "Joshua Bloch", "published_year": 2017, "genre": "プログラミング"},
    {"title": "Clean Code", "author": "Robert C. Martin", "published_year": 2008, "genre": "ソフトウェア工学"},
    {"title": "Fluent Python", "author": "Luciano Ramalho", "published_year": 2015, "genre": "プログラミング"},
    {"title": "独習C++", "author": "佐藤一郎", "published_year": 2010, "genre": "プログラミング"},
    {"title": "未来の物語", "author": "田中花子", "published_year": 2024, "genre": "フィクション"},
    {"title": "データベース実践", "author": "高橋次郎", "published_year": 2021, "genre": "DB"},
]

SAMPLE_MEMBERS = [
    {"name": "佐藤太郎", "age": 25, "email": "sato@example.com", "days_ago": 3},
    {"name": "鈴木花子", "age": 30, "email": "suzuki@example.com", "days_ago": 7},
    {"name": "田中一郎", "age": 22, "email": "tanaka@example.com", "days_ago": 15},
    {"name": "高橋次郎", "age": 28, "email": "takahashi@example.com", "days_ago": 30},
    {"name": "伊藤美咲", "age": 35, "email": "ito@example.com", "days_ago": 45},
    {"name": "渡辺健", "age": 40, "email": "watanabe@example.com", "days_ago": 60},
    {"name": "山本さくら", "age": 27, "email": "yamamoto@example.com", "days_ago": 90},
    {"name": "中村拓海", "age": 24, "email": "nakamura@example.com", "days_ago": 120},
    {"name": "小林美和", "age": 29, "email": "kobayashi@example.com", "days_ago": 150},
    {"name": "加藤大輔", "age": 33, "email": "kato@example.com", "days_ago": 180},
]

def main(reset=False):
    initialize_database()

    if reset:
        print("既存のレコードを削除します...")
        try:
            Borrow.delete().execute()
            Member.delete().execute()
            Book.delete().execute()
        except Exception as e:
            print("削除時にエラー:", e)
            return

    # 本のデータ挿入
    existing_books = Book.select().count()
    if existing_books > 0 and not reset:
        print(f"既に Book テーブルに {existing_books} 件存在します。")
    else:
        inserted_books = 0
        for b in SAMPLE_BOOKS:
            try:
                Book.create(
                    title=b.get("title"),
                    author=b.get("author"),
                    published_year=ensure_int(b.get("published_year")),
                    genre=b.get("genre"),
                )
                inserted_books += 1
            except Exception as e:
                print("挿入に失敗したレコード:", b, "エラー:", e)
        print(f"本のサンプルデータを挿入しました（{inserted_books} 件）。")

    # 会員のデータ挿入
    existing_members = Member.select().count()
    if existing_members > 0 and not reset:
        print(f"既に Member テーブルに {existing_members} 件存在します。")
    else:
        inserted_members = 0
        now = datetime.now()
        for m in SAMPLE_MEMBERS:
            try:
                # 登録日時を過去にずらす
                days_ago = m.get("days_ago", 0)
                registration_date = now - timedelta(days=days_ago)
                
                Member.create(
                    name=m.get("name"),
                    age=ensure_int(m.get("age")),
                    email=m.get("email"),
                    created_at=registration_date
                )
                inserted_members += 1
            except Exception as e:
                print("挿入に失敗したレコード:", m, "エラー:", e)
        print(f"会員のサンプルデータを挿入しました（{inserted_members} 件）。")

    # 貸出データのサンプル挿入（オプション）
    existing_borrows = Borrow.select().count()
    if existing_borrows == 0:
        print("貸出データのサンプルを作成中...")
        members = list(Member.select())
        books = list(Book.select())

        if members and books:
            inserted_borrows = 0
            for _ in range(15):  # 15件の貸出データ
                try:
                    member = random.choice(members)
                    book = random.choice(books)
                    days_ago = random.randint(1, 120)
                    borrow_date = datetime.now() - timedelta(days=days_ago)

                    Borrow.create(
                        member=member,
                        book=book,
                        borrow_date=borrow_date
                    )
                    inserted_borrows += 1
                except Exception as e:
                    print("貸出データ挿入エラー:", e)
            print(f"貸出のサンプルデータを挿入しました（{inserted_borrows} 件）。")

if __name__ == "__main__":
    reset_flag = "--reset" in sys.argv or "-r" in sys.argv
    main(reset=reset_flag)