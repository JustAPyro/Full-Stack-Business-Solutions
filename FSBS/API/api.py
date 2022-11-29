from .endpoints import ep_users, ep_auth, ep_purchases
from .structures import models
from FSBS.API.database.database import engine
from fastapi import FastAPI, Depends
from .dependencies import get_db, get_current_user


# Generate database tables (Later convert this to Alembic)
models.Base.metadata.create_all(bind=engine)

# Instantiate the API server
api = FastAPI(dependencies=[Depends(get_db)])

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
