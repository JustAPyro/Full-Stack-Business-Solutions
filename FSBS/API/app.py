import os
from flask import Flask
from FSBS.API.routes import register_urls
from FSBS.API.extensions import db, bcrypt



def create_api():
    # Create API app
    api = Flask(__name__)

    # Configure... the configs
    api.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URL",
                                                           "postgresql://postgres:defaultpassword@localhost/fsbs_development")

    # Register information to run api
    register_extensions(api)
    register_models(api)
    register_urls(api)

    # Return the api object
    return api


def register_models(api):
    with api.app_context():
        db.create_all()


def register_extensions(api):
    db.init_app(api)
    bcrypt.init_app(api)




if __name__ == "__main__":
    create_api().run()
