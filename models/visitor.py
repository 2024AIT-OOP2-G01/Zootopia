from peewee import Model, IntegerField, DateField
from .db import db

class Visitor(Model):
    date = DateField()
    male = IntegerField()
    female = IntegerField()
    boy = IntegerField()
    girl = IntegerField()

    class Meta:
        database = db