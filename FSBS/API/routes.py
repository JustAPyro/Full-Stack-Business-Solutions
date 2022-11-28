from FSBS.API.decorators import user_endpoint
from FSBS.API.endpoints.transaction_endpoints import (
    transaction_endpoint,
    transactions_endpoint)
from FSBS.API.endpoints.auth_endpoints import *



def hello():
    return '{"message": "Hello world!"}'


def register_urls(api):
    api.add_url_rule('/', methods=['GET', 'POST'], view_func=hello)
    api.add_url_rule('/register', methods=['POST'], view_func=register_user)
    api.add_url_rule('/authorize', methods=['POST'], view_func=authorize_user)
    api.add_url_rule('/transaction', methods=['GET', 'POST'], view_func=transaction_endpoint)
    api.add_url_rule('/transactions', methods=['GET', 'POST'], view_func=transactions_endpoint)
