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
        animal_kind_id = request.form['animal_kind_id']
        role_date = datetime.now()
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
    return render_template('order_edit.html', role=role, keepers=keepers, animals=animals, kinds=kinds)


@role_bp.route('/api/count_kind')
def count_kind():
    query = (User
             .select(User.name, fn.COUNT(Role.id).alias('count'))
             .join(Role, on=(Role.keeper == User.id))
             .group_by(User.name))

    data = {
        "labels": [r.name for r in query],
        "data": [r.count for r in query]
    }
    return jsonify(data)
