from flask import Flask
from extensions import db, bcrypt
from config import current_config
from secrets import secrets
from routes import (
    test_func,
    register_user,
    authorize_user,
    transaction_post
)


def create_api(config_object=current_config):
    # Create API app
    api = Flask(__name__)

    # Configure... the configs
    api.config.from_object(config_object)
    # api.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{secrets["db_user"]}:{secrets["db_pass"]}@localhost/{api.config.get("DB_NAME")}'
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
    api.add_url_rule('/test', methods=['GET', 'POST'], view_func=test_func)
    api.add_url_rule('/register', methods=['POST'], view_func=register_user)
    api.add_url_rule('/authorize', methods=['POST'], view_func=authorize_user)
    api.add_url_rule('/transaction', methods=['POST'], view_func=transaction_post)


if __name__ == '__main__':
    create_api().run()


