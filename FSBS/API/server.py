from fastapi import FastAPI
from .database.database import engine
from .structures import models
from .api import api

# Generate database tables (Later convert this to Alembic)
models.Base.metadata.create_all(bind=engine)

# Instantiate the API server
server = FastAPI(
    #dependencies=[Depends(get_db)]
    )

#api.add_middleware(BaseHTTPMiddleware, dispatch=track_api)

# Routers for each subset of endpoints
#api.include_router(ep_users.router)
#api.include_router(ep_purchases.router)
#api.include_router(ep_auth.router)

server.include_router(api)

@server.get("/")
async def root():
    return {"message": "Hello World"}

