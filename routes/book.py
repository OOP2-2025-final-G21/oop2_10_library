from flask import Blueprint, render_template, request, redirect, url_for
from models import Book

book_bp = Blueprint('book', __name__, url_prefix='/books')

# 一覧表示
@book_bp.route('/')
def list():
    books = Book.select()
    return render_template('book_list.html', title='本一覧', items=books)

# 新規登録
@book_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
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
        return redirect(url_for('book.list'))

    return render_template('book_add.html')


# 編集
@book_bp.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit(book_id):
    book = Book.get_or_none(Book.id == book_id)
    if not book:
        return redirect(url_for('book.list'))

    if request.method == 'POST':
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.published_year = int(request.form.get('published_year'))
        book.genre = request.form.get('genre')
        book.save()
        return redirect(url_for('book.list'))

    return render_template('book_edit.html', book=book)
