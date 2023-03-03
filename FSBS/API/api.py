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


# --- Order API's ---
@raw_api.get('/order')
def get_order():
    return "order"

@raw_api.post('/order')
def post_order():
    return None

@raw_api.put('/order')
def put_order():
    return None

@raw_api.delete('/order')
def delete_order():
    return None
