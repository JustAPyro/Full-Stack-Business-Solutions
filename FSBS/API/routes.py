from flask import request

def names():
    return '{"name": "Luke", "last": "Hanna", "dob": "10/02/1997"}'


def create_user():
    return request.form.get('username')
