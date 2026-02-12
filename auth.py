import logging
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('exam.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('exam.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=False)  # Session expires on browser close
            next_page = request.args.get('next')
            logging.debug(f"User {user.username} logged in successfully")
            return redirect(next_page if next_page else url_for('exam.dashboard'))
        else:
            flash('Invalid email or password', 'danger')
            logging.debug("Login failed: invalid credentials")
    
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('exam.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if email already exists
        existing_user = User.objects(email=form.email.data).first()
        if existing_user:
            flash('Email already registered', 'danger')
            return render_template('register.html', form=form)
        
        # Check if username already exists
        existing_user = User.objects(username=form.username.data).first()
        if existing_user:
            flash('Username already taken', 'danger')
            return render_template('register.html', form=form)
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            department=form.department.data,
            is_faculty=True  # All users are faculty in this system
        )
        user.set_password(form.password.data)
        user.save()
        
        flash('Registration successful! Please log in.', 'success')
        logging.debug(f"New user registered: {user.username}")
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
