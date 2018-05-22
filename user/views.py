from flask import Blueprint, render_template, request, redirect, session
import bcrypt

from user.forms import RegisterForm, LoginForm
from user.models import User
from application import db

user_app = Blueprint('user_app', __name__)

@user_app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf8'), bcrypt.gensalt())
        user = User(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    username=form.username.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return 'User Registered'
    return render_template('user/register.html', form=form)

@user_app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            password_check = bcrypt.checkpw(form.password.data.encode('utf8'), user.password)
            if password_check:
                session['username'] = form.username.data
                return 'User Logged In'
            else:
                user = None #if password fails overwrite previous user
        if not user: # this structure necessary to avoid username guessing
            error = 'Invalid credentials'
    return render_template('user/login.html', form=form, error=error)
