from flask import Blueprint, render_template, request, redirect, url_for
from models import Borrow, Member, Book
from datetime import datetime

# Blueprintの作成
borrow_bp = Blueprint('borrow', __name__, url_prefix='/borrows')


@borrow_bp.route('/')
def list():
    borrows = Borrow.select()
    return render_template('borrow_list.html', title='貸出一覧', items=borrows)


@borrow_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        member_id = request.form['member_id']
        book_id = request.form['book_id']
        borrow_date = datetime.now()
        Borrow.create(member=member_id, book=book_id, borrow_date=borrow_date)
        return redirect(url_for('borrow.list'))
    
    members = Member.select()
    books = Book.select()
    return render_template('borrow_add.html', members=members, books=books)


@borrow_bp.route('/edit/<int:borrow_id>', methods=['GET', 'POST'])
def edit(borrow_id):
    borrow = Borrow.get_or_none(Borrow.id == borrow_id)
    if not borrow:
        return redirect(url_for('borrow.list'))

    if request.method == 'POST':
        borrow.member = request.form['member_id']
        borrow.book = request.form['book_id']
        borrow.save()
        return redirect(url_for('borrow.list'))

    members = Member.select()
    books = Book.select()
    return render_template('borrow_edit.html', borrow=borrow, members=members, books=books)
