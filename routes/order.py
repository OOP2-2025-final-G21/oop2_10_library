from flask import Blueprint, render_template, request, redirect, url_for
from models import Order, Member, Product
from datetime import datetime

# Blueprintの作成
order_bp = Blueprint('order', __name__, url_prefix='/orders')


@order_bp.route('/')
def list():
    orders = Order.select()
    return render_template('order_list.html', title='注文一覧', items=orders)


@order_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        member_id = request.form['member_id']
        product_id = request.form['product_id']
        order_date = datetime.now()
        Order.create(member=member_id, product=product_id, order_date=order_date)
        return redirect(url_for('order.list'))
    
    members = Member.select()
    products = Product.select()
    return render_template('order_add.html', members=members, products=products)


@order_bp.route('/edit/<int:order_id>', methods=['GET', 'POST'])
def edit(order_id):
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return redirect(url_for('order.list'))

    if request.method == 'POST':
        order.member = request.form['member_id']
        order.product = request.form['product_id']
        order.save()
        return redirect(url_for('order.list'))

    members = Member.select()
    products = Product.select()
    return render_template('order_edit.html', order=order, members=members, products=products)
