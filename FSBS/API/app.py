import os
from flask import Flask
from extensions import db, bcrypt
from routes import (
    hello,
    register_user,
    authorize_user,
    transaction_post
)


def create_api():
    # Create API app
    api = Flask(__name__)

    # Configure... the configs
    api.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URL", "Default")

    # Register information to run api
    register_extensions(api)
    register_models(api)
    register_urls(api)

    # Return the api object
    return api


def register_models(api):
    with api.app_context():
        from models import (
            User,
            Transaction)
        db.create_all()


def register_extensions(api):
    db.init_app(api)
    bcrypt.init_app(api)


def register_urls(api):
    api.add_url_rule('/', methods=['GET', 'POST'], view_func=hello)
    api.add_url_rule('/register', methods=['POST'], view_func=register_user)
    api.add_url_rule('/authorize', methods=['POST'], view_func=authorize_user)
    api.add_url_rule('/transaction', methods=['POST'], view_func=transaction_post)


app = create_api()


