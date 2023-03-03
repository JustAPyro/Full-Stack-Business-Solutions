from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Create the router
web = APIRouter(tags=['Webpage'])

# Load jinja templates and mount static files (E.g. bootstrap)
templates = Jinja2Templates(directory='FSBS/API/templates')

@web.get('/sign-in')
def sign_in(request: Request):
    return templates.TemplateResponse('sign_in.html', {'request': request})
