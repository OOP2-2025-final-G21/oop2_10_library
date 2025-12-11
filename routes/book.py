from flask import Blueprint, render_template, request, redirect
from models.book import Book

bp = Blueprint('books', __name__, url_prefix='/books')

# 一覧表示
@bp.route('/')
def list_books():
    books = Book.select()
    return render_template('books/list.html', books=books)

# 新規登録フォーム
@bp.route('/new')
def new_book():
    return render_template('books/new.html')

# 新規登録処理
@bp.route('/create', methods=['POST'])
def create_book():
    title = request.form.get('title')
    author = request.form.get('author')
    published_year = request.form.get('published_year')
    genre = request.form.get('genre')

    Book.create(
        title=title,
        author=author,
        published_year=int(published_year),
        genre=genre
    )

    return redirect('/books')

# 編集フォーム
@bp.route('/edit/<int:id>')
def edit_book(id):
    book = Book.get_or_none(Book.id == id)
    if not book:
        return redirect('/books')
    return render_template('books/edit.html', book=book)

# 編集更新処理
@bp.route('/update/<int:id>', methods=['POST'])
def update_book(id):
    book = Book.get_or_none(Book.id == id)
    if not book:
        return redirect('/books')

    book.title = request.form.get('title')
    book.author = request.form.get('author')
    book.published_year = int(request.form.get('published_year'))
    book.genre = request.form.get('genre')

    book.save()
    return redirect('/books')

# 削除処理
@bp.route('/delete/<int:id>', methods=['POST'])
def delete_book(id):
    book = Book.get_or_none(Book.id == id)
    if book:
        book.delete_instance()
    return redirect('/books')
