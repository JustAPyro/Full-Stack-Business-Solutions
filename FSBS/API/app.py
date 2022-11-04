from flask import Flask
from extensions import db, bcrypt
from routes import (
    hello,
    test_func,
    register_user,
    authorize_user,
    transaction_post
)


def create_api():
    # Create API app
    api = Flask(__name__)

    # Configure... the configs
    api.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gxxgezcatnkide:9ab7f8472e5f4e3131d2981ac03cee086b016513783a58d8c7d7cf1aa5fa09c9@ec2-44-210-228-110.compute-1.amazonaws.com:5432/d1cdnfqhn9j845'

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
    api.add_url_rule('/', methods=['GET'], view_func=hello)
    api.add_url_rule('/test', methods=['GET', 'POST'], view_func=test_func)
    api.add_url_rule('/register', methods=['POST'], view_func=register_user)
    api.add_url_rule('/authorize', methods=['POST'], view_func=authorize_user)
    api.add_url_rule('/transaction', methods=['POST'], view_func=transaction_post)


app = create_api()

