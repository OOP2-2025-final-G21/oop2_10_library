from .user import user_bp
from .book import book_bp
from .borrow import borrow_bp

# Blueprintをリストとしてまとめる
blueprints = [
  user_bp,
  book_bp,
  borrow_bp
]
