from .user import user_bp
from .book import book_bp
from .order import order_bp

# Blueprintをリストとしてまとめる
blueprints = [
  user_bp,
  book_bp,
  order_bp
]
