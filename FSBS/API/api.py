from flask import Flask
from extensions import db, bcrypt
from config import current_config
from secrets import secrets
from routes import names


def create_api(config_object=current_config):
    # Create API app
    api = Flask(__name__)

    # Configure... the configs
    api.config.from_object(config_object)
    api.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{secrets["db_user"]}:{secrets["db_pass"]}@localhost/{api.config.get("DB_NAME")}'

    # Register information to run api
    register_extensions(api)
    register_models(api)
    register_urls(api)

    # Return the api object
    return api


def register_models(api):
    with api.app_context():
        from models import User
        db.create_all()
        db.session.add(User("Luke", "bacon"))
        db.session.commit()


def register_extensions(api):
    db.init_app(api)
    bcrypt.init_app(api)


def register_urls(api):
    api.add_url_rule('/names.api', 'names', names)


if __name__ == '__main__':
    create_api().run()
