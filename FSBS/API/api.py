from fastapi import APIRouter

act_api = APIRouter(
    prefix='/api/action',
    tags=['Actions']
)

# ------------------------- Raw API --------------

raw_api = APIRouter(
    prefix='/api'
)

@raw_api.post('/users')
def post_users():
    return "check"
