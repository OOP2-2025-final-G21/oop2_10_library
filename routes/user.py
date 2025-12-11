from flask import Blueprint, render_template, request, redirect, url_for
from models import Member

# Blueprintの作成
user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route('/')
def list():

    # データ取得
    members = Member.select()

    return render_template('user_list.html', title='メンバー一覧', items=members)


@user_bp.route('/add', methods=['GET', 'POST'])
def add():

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        Member.create(name=name, age=age, email=email)
        return redirect(url_for('user.list'))

    return render_template('user_add.html')


@user_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    member = Member.get_or_none(Member.id == user_id)
    if not member:
        return redirect(url_for('user.list'))

    if request.method == 'POST':
        member.name = request.form['name']
        member.age = request.form['age']
        member.email = request.form['email']
        member.save()
        return redirect(url_for('user.list'))

    return render_template('user_edit.html', user=member)