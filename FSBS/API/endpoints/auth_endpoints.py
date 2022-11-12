import json

from flask import request, Response


def authorize_user():
    # Collect data
    data = request.get_json()

    if not data:
        return Response(
            response=json.dumps({
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"}),
            status=400,
            content_type='JSON')

    email = data['email']
    password = data['password']

    # Process the email by forcing it to lower
    email = email.lower()

    # Find the user in the database
    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):

        # get the token
        auth_token = user.encode_auth_token(user.user_id)


        if auth_token:
            return Response(
                response=json.dumps({'auth_token': auth_token}),
                status=200,
                content_type='JSON')
        else:
            return Response(
                response=json.dumps({'ERROR': 'User does not exist.'}),
                status=404,
                content_type='JSON')

    return Response(  # TODO: Add a better response here
        response=json.dumps({'ERROR': "User could not be found."}),
        status=401,
        content_type='JSON')