import random

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from .models import User
from . import *

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        flash('Please check credentials and try again')
        return redirect(url_for('auth.login'))

    if not check_password_hash(user.password, password):
        flash('Please check your password and try again')
        return redirect(url_for('auth.login'))
    login_user(user)
    return redirect(url_for('main.dashboard'))

@auth.route('/register')
def register():
    return render_template('register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    user_id = random.randint(111, 999)
    name = request.form.get('name')
    vat_pin = request.form.get('vat_pin')
    email = request.form.get('email')
    address = request.form.get('address')
    phone = request.form.get('phone')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.register'))

    user1 = User.query.filter_by(name=name).first()

    if user1:
        flash('Business already registerd')
        return redirect(url_for('auth.register'))

    user2 = User.query.filter_by(vat_pin=vat_pin).first()

    if user2:
        flash('VAT Pin already registerd')
        return redirect(url_for('auth.register'))

    new_user = User(user_id=user_id, name=name, vat_pin=vat_pin, email=email, address=address, phone=phone, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()
    flash('Account creation successful')
    return redirect(url_for('auth.login'))



