from fastapi import APIRouter

api = APIRouter(
    prefix='/api/action',
    tags=['Actions']
)