from peewee import Model, ForeignKeyField, DateTimeField
from .db import db
from .user import User
from .product import Product

class Role(Model):
    keeper = ForeignKeyField(User, backref='keepers')#飼育員の名前
    animalname = ForeignKeyField(Product, backref='animal_names')#動物の愛称
    role_date = DateTimeField()

    class Meta:
        database = db
