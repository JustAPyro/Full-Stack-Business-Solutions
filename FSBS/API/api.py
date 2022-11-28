from flask import Flask
from FSBS.API.routes import register_urls
from FSBS.API.extensions import bcrypt
from FSBS.API.database import models
from FSBS.API.database.database import SessionLocal, engine
from fastapi import FastAPI, Depends
from .dependencies import get_db
from FSBS.API.endpoints import ep_users

# Generate database tables (Later convert this to Alembic)
models.Base.metadata.create_all(bind=engine)

# Instantiate the API server
api = FastAPI(dependencies=[Depends(get_db)])

# Routers for each subset of endpoints
api.include_router(ep_users.router)



@api.get("/")
async def root():
    return {"message": "Hello World"}


# POST /api/users -> Create user
# GET /api/users/{id} -> Get USER
# DELETE /api/users/{id} -> Delete user


def create_api():
    # Create API app
    api = Flask(__name__)

    # Configure... the configs
    api.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgreSQLpassword@localhost/fsbs_development"

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
