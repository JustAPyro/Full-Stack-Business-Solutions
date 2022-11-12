
def validate_exists(data: dict, *args):
    missing = []
    for item in args:
        if item not in data:
            missing.append(item)
    return len(missing) == len(args), missing

