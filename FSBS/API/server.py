from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .web import web

# Generate database tables (Later convert this to Alembic)
# models.Base.metadata.create_all(bind=engine)

# Instantiate the API server
server = FastAPI(
    #dependencies=[Depends(get_db)]
)

# Load jinja templates and mount static files (E.g. bootstrap)
templates = Jinja2Templates(directory='FSBS/API/templates')
server.mount('/static', StaticFiles(directory='FSBS/API/static'), name='static')

#api.add_middleware(BaseHTTPMiddleware, dispatch=track_api)

# Routers for each subset of endpoints
#api.include_router(ep_users.router)
#api.include_router(ep_purchases.router)
#api.include_router(ep_auth.router)

# server.include_router(raw_api)
# server.include_router(act_api)
server.include_router(web)


@server.get("/")
async def root():
    return {"message": "Hello World"}

