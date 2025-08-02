from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from ..models import User, db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        role = request.form.get('role')

        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists.', 'warning')
            return redirect(url_for('auth.register'))

        # Create new user
        new_user = User(email=email, name=name, phone_number=phone_number, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('main.index'))

    return render_template('auth/register.html', title='Register')

@auth.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        login_user(user, remember=True)
        return redirect(url_for('main.dashboard'))
    else:
        flash('Login Unsuccessful. Please check email and password.', 'danger')
        return redirect(url_for('main.index'))

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))