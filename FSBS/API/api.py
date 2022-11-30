from fastapi import FastAPI, Depends
from starlette.middleware.base import BaseHTTPMiddleware

from .endpoints import ep_users, ep_auth, ep_purchases
from .database.database import engine
from .dependencies import get_db
from .structures import models
from .middleware import track_api


# Generate database tables (Later convert this to Alembic)
models.Base.metadata.create_all(bind=engine)

# Instantiate the API server
api = FastAPI(dependencies=[Depends(get_db)])

api.add_middleware(BaseHTTPMiddleware, dispatch=track_api)

# Routers for each subset of endpoints
api.include_router(ep_users.router)
api.include_router(ep_purchases.router)
api.include_router(ep_auth.router)


@api.get("/")
async def root():
    return {"message": "Hello World"}


@api.get("/status")
async def status():
    return {"status": "200/okay"}
