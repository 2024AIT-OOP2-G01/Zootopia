from flask import Blueprint, render_template, request, redirect, url_for
from models import Product
from flask import jsonify
from peewee import fn

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
  
@product_bp.route('/api/animal_ratio')
def get_animal_ratio():
    # 各 product.name の出現回数を集計
    product_counts = Product.select(Product.kind, fn.COUNT(Product.id).alias('count')).group_by(Product.kind)

    # 総数を計算
    total_count = sum([p.count for p in product_counts])

    # データを割合に変換
    data = {
        "labels": [p.kind for p in product_counts],
        "data": [p.count for p in product_counts],  # 絶対数を送信
    }

    return jsonify(data)
