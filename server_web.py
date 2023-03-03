from fastapi import APIRouter, Request



# Create the router
web = APIRouter(tags=['Webpage'])

# Import jinja templates
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory='templates')

@web.get('/sign-in')
def sign_in(request: Request):
    return templates.TemplateResponse('sign_in.html', {'request': request})
