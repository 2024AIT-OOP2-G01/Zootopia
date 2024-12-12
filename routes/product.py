from flask import Blueprint, render_template, request, redirect, url_for
from models import Product

# Blueprintの作成
product_bp = Blueprint('product', __name__, url_prefix='/products')


@product_bp.route('/')
def list():
    products = Product.select()
    print(products)
    return render_template('product_list.html', title='動物一覧', items=products)


@product_bp.route('/add', methods=['GET', 'POST'])
def add():

    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        kind = request.form['kind']
        name = request.form['name']
        food = request.form['food']

        Product.create(kind=kind, name=name, food=food)
        return redirect(url_for('product.list'))

    return render_template('product_add.html')


@product_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit(product_id):
    product = Product.get_or_none(Product.id == product_id)
    if not product:
        return redirect(url_for('product.list'))

    if request.method == 'POST':
        product.kind = request.form['kind']
        product.name = request.form['name']
        product.food = request.form['food']
        product.save()
        return redirect(url_for('product.list'))

    return render_template('product_edit.html', product=product)
