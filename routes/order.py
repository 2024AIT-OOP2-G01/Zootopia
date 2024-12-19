from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import User, Product, Role
from datetime import datetime
from peewee import fn

# Blueprintの作成
role_bp = Blueprint('role', __name__, url_prefix='/roles')


@role_bp.route('/')
def list():
    roles = Role.select()
    print(roles)
    return render_template('order_list.html', title='飼育表', items=roles)


@role_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        keeper_id = request.form['keeper_id']
        animal_id = request.form['animal_id']
        role_date = datetime.now()
        animal_kind_id = request.form['animal_kind_id']
        Role.create(keeper=keeper_id, animalname=animal_id, role_date=role_date,animal_kind = animal_kind_id)
        return redirect(url_for('role.list'))

    keepers = User.select()
    animals = Product.select()
    kinds = Product.select()
    return render_template('order_add.html', keepers=keepers, animals=animals,kinds = kinds)



@role_bp.route('/edit/<int:role_id>', methods=['GET', 'POST'])
def edit(role_id):
    role = Role.get_or_none(Role.id == role_id)
    if not role:
        return redirect(url_for('role.list'))

    if request.method == 'POST':
        role.keeper = User.get(User.id == request.form['keeper_id'])
        role.animalname = Product.get(Product.id == request.form['animal_id'])
        role.animal_kind_id = Product.get(Product.id == request.form['animal_kind_id'])
        role.role_date = datetime.now()
        role.save()

        return redirect(url_for('role.list'))

    keepers = User.select()
    animals = Product.select()
    kinds = Product.select()
    return render_template('order_edit.html', role=role, keepers=keepers, animals=animals,kinds=kinds)



@role_bp.route('/api/count_kind')
def count_kind():
    from collections import defaultdict

    query = (User
        .select(User.name, Product.kind, fn.COUNT(Role.id).alias('count'))
        .join(Role, on=(Role.keeper == User.id))
        .join(Product, on=(Role.animalname == Product.id))
        .group_by(User.name, Product.kind)
        .dicts())  # ここでdicts()を呼ぶ

    user_set = set()
    kind_set = set()
    data_map = defaultdict(lambda: defaultdict(int))

    for row in query:
        # rowは辞書になるので、'name', 'kind', 'count'キーでアクセスできる
        user_name = row['name']
        animal_kind = row['kind']
        count = row['count']

        user_set.add(user_name)
        kind_set.add(animal_kind)
        data_map[user_name][animal_kind] = count

    users = sorted(user_set)
    kinds = sorted(kind_set)

    background_colors = [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)'
    ]

    border_colors = [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
    ]

    datasets = []
    for i, k in enumerate(kinds):
        datasets.append({
            "label": k,
            "data": [data_map[u][k] for u in users],
            "backgroundColor": background_colors[i % len(background_colors)],
            "borderColor": border_colors[i % len(border_colors)],
            "borderWidth": 1
        })

    data = {
        "labels": users,
        "datasets": datasets
    }
    return jsonify(data)