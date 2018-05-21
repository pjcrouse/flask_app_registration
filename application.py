from flask import Flask, render_template, url_for, request, session, redirect
from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError
import bcrypt
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('settings.py')
    db = SQLAlchemy(app)

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(80), nullable=False)
        last_name = db.Column(db.String(80), nullable=False)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password = db.Column(db.String, nullable=False)

        def __repr__(self):
            return f'<User {self.username}>'

    class RegisterForm(FlaskForm):
        first_name = StringField('First Name', [validators.Required()])
        last_name = StringField('Last Name', [validators.Required()])
        email = EmailField('Email Address', [validators.DataRequired(),
                                            validators.Email()])
        username = StringField('Username', [validators.Required(),
                                            validators.length(min=4, max=25)])
        password = PasswordField('New Password', [validators.Required(),
                                                 validators.EqualTo('confirm',
                                                    message='Passwords must match'),
                                                 validators.length(min=4, max=80)])
        confirm = PasswordField('Repeat Password')

        # custom validators implement once i get the db up
        def validate_username(form, field):
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('Username already exists')

        def validate_email(form, field):
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('Email already in use')

    class LoginForm(FlaskForm):
        username = StringField('Username', [validators.Required()])
        password = PasswordField('Password', [validators.Required()])

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/register', methods=('GET', 'POST'))
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
        return render_template('register.html', form=form)

    @app.route('/login', methods=('GET', 'POST'))
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
        return render_template('login.html', form=form, error=error)

    return app
