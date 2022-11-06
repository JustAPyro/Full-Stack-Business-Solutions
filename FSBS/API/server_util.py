





valid_content_types = [
    'application/json'
]


def get_request_data(content_type: str, request) -> dict[str, str]:
    if content_type not in valid_content_types:
        raise Exception(f"Request content type unknown: {content_type}")

    if content_type == 'application/js':
        # Start by trying to get the json format data
        data = request.get_json()

        if not data:  # If there's no data in the request raise an error
            raise Exception('No payload data in this request!')

        # Parse the json

