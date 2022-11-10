import json

from extensions import db
from flask import request, Response
from models import User, Transaction
from FSBS.API import errors


def transaction_endpoint():
    method_endpoints = {
        'GET': transaction_GET,
        'POST': transaction_POST}
    return method_endpoints[request.method]()


def transactions_endpoint():
    method_endpoints = {
        'GET': transactions_GET,
        'POST': transactions_POST}
    return method_endpoints[request.method]()


def transaction_GET():
    # Start by trying to get the requesting user
    success, user, error_response = User.get_user(request)

    # If the user couldn't be validated return an error
    if not success:
        return error_response

    # Try checking for a transaction_id
    tid = request.args.to_dict().get('transactionid')

    # If there's no transaction id then throw an error response
    if not tid:
        return errors.MISSING_PARAMS(params='transactionid', data=request.json)

    # Now find the transaction
    transaction = Transaction.query.filter_by(transaction_id=tid).first()

    # If the transaction doesn't belong to this user throw another error
    if user != transaction.user:
        return errors.USER_NOT_AUTHORIZED('Transaction', request.json)

    # Otherwise return the transaction
    return Response(
        response=transaction.to_json(),
        status=200,
        content_type='JSON'
    )


def transaction_POST():
    # Start by trying to get the requesting user
    success, user, error_response = User.get_user(request)

    # If the user couldn't be validated return an error
    if not success:
        return error_response

    # Now get the json from the request
    data = request.get_json()

    # If there's no data throw an error
    if not data:
        return errors.MISSING_BODY(request.json)

    # Unpack the rest of the information from the request
    location = data.get('location')
    cost = data.get('cost')
    tax = data.get('tax')
    purchase_time = data.get('time', None)

    # Validate data and if it is invalid return a malformed body error
    valid, issues = Transaction.validator(location, cost, tax, purchase_time)
    if not valid: return errors.MALFORMED_BODY(issues, {}, request=request)

    # Create a transaction
    transaction = Transaction(user.user_id,
                              location=location,
                              cost=cost,
                              tax=tax,
                              purchase_time=purchase_time)

    # Insert the transaction in the database
    db.session.add(transaction)
    db.session.commit()

    return Response(
        response="Success",
        status=200,
        content_type='JSON')


def transactions_GET():
    # Start by trying to get the requesting user
    success, user, error_response = User.get_user(request)

    # If the user couldn't be validated return an error
    if not success:
        return error_response

    # Get the list of transactions
    transactions = user.transactions

    # create a list of transaction dicts
    transaction_map = list()
    for t in transactions:
        transaction_map.append(t.to_dict())

    # Convert the list into json
    transaction_json = json.dumps(transaction_map)

    # Return the list
    return Response(
        response=transaction_json,
        status=200,
        content_type='JSON')


def transactions_POST():
    # Start by trying to get the requesting user
    success, user, error_response = User.get_user(request)

    # If the user couldn't be validated return an error
    if not success:
        return error_response

    # Now get the json from the request
    data = request.get_json()

    # If there's no data throw an error
    if not data:
        return errors.MISSING_BODY(data=request.json)

    # Unpack the rest of the information from the request
    for t in data:
        location = t['location']
        cost = t['cost']
        tax = t['tax']
        purchase_time = t.get('time', None)

        # Validate data and if it is invalid return a malformed body error
        valid, issues = Transaction.validator(location, cost, tax, purchase_time)
        if not valid: return errors.MALFORMED_BODY(issues=issues, data={})

        # Create a transaction
        transaction = Transaction(user.user_id,
                                  location=location,
                                  cost=cost,
                                  tax=tax,
                                  purchase_time=purchase_time)

        # Insert the transaction in the database
        db.session.add(transaction)

    # Commit all the added transactions
    db.session.commit()

    return Response(
        response="Success",
        status=200,
        content_type='JSON')
