def validate_exists(data: dict, *args):
    missing = []
    for item in args:
        if item not in data:
            missing.append(item)
    return len(missing) == len(args), missing


def user_validator(email, password, first_name, last_name, phone=None, data=None):
    # flag for valid
    valid = True

    # Map to store the issues in
    validation_errors = dict()
    validation_errors['missing'] = list()

    # Check to make sure all the required features exist
    for feature in ['email', 'password', 'first_name', 'last_name']:
        if not data[feature]: validation_errors['missing'].append(feature); valid = False

    # TODO: Fix this
    # If the email already exists
    # if db.session.query(db.exists().where(User.email == data['email'])).scalar():
    #    validation_errors['exists'] = ['email'];
    #    valid = False

    return valid, validation_errors
