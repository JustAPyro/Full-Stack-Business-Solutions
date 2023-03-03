from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

from dependencies import database
from server_web import web
from server_api import api

# Instantiate the API server
server = FastAPI(dependencies=[Depends(database)])

# Mount the static files we server (Images, javascript files, bootstrap)
server.mount('/static', StaticFiles(directory='static'), name='static')

server.include_router(api)
server.include_router(web)


@server.get("/")
async def root():
    return {"message": "Hello World"}

