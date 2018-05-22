from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError
import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(**config_overrides):
    app = Flask(__name__)

    app.config.from_pyfile('settings.py')
    app.config.update(config_overrides)
    from user.views import user_app
    db.init_app(app)
    app.register_blueprint(user_app)

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    return app
