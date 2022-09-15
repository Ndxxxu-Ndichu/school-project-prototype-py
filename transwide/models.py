from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(100), unique=True)
    vat_pin = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    address = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    password = db.Column(db.String(255))

class Quotations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer)
    creator = db.Column(db.String(100))
    date = db.Column(db.String(100))
    item_name = db.Column(db.String(100))
    item_quantity = db.Column(db.Integer)

class AllQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.String(100))
    quotation_id = db.Column(db.Integer)
    date = db.Column(db.String(100))

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer)
    creator = db.Column(db.String(100), default="Admin")
    date = db.Column(db.String(100))
    item_name = db.Column(db.String(100))
    item_quantity = db.Column(db.Integer)
    item_price = db.Column(db.Integer)
    item_total = db.Column(db.Integer)




