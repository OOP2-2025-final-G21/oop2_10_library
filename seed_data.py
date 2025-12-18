import os
import sys

# スクリプトをプロジェクトルートから実行することを想定
# (VS Code のターミナルで project root に移動して実行してください)
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from models import initialize_database
try:
    from models import Book
except Exception as e:
    print("models.Book のインポートに失敗しました:", e)
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

def main(reset=False):
    initialize_database()

    if reset:
        print("既存の Book レコードを削除します...")
        try:
            Book.delete().execute()
        except Exception as e:
            print("削除時にエラー:", e)
            return

    existing = Book.select().count()
    if existing > 0 and not reset:
        print(f"既に Book テーブルに {existing} 件存在します。新規挿入をスキップします（--reset で上書き可能）。")
        return

    inserted = 0
    for b in SAMPLE_BOOKS:
        try:
            Book.create(
                title=b.get("title"),
                author=b.get("author"),
                published_year=ensure_int(b.get("published_year")),
                genre=b.get("genre"),
            )
            inserted += 1
        except Exception as e:
            print("挿入に失敗したレコード:", b, "エラー:", e)

    print(f"サンプルデータを挿入しました（{inserted} 件）。")

if __name__ == "__main__":
    reset_flag = "--reset" in sys.argv or "-r" in sys.argv
    main(reset=reset_flag)