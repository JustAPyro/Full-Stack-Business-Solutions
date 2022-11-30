import datetime
import time
from fastapi import Request
from FSBS.API.dependencies import get_db, get_current_user
from FSBS.API.database import database_interface as dbi
from FSBS.API.structures import schemas
from FSBS.API.utility.formatting import stringify_params


async def track_api(request: Request, call_next):

    response = await call_next(request)

    user_id = None
    try:
        user = await get_current_user(request.headers['authorization'].split(' ')[1])
        user_id = user.user_id
    except Exception as e:
        print(e)

    dbi.submit_request(next(get_db()),
                       schemas.APIRequestCreate(
                           user_id=user_id,
                           method=request.method,
                           endpoint=request.url.path,
                           query=request.url.query,
                           params=None if len(request.path_params) == 0 else request.path_params,
                           body=None,
                           time=datetime.datetime.now(),
                           caller_ip=request.client.host,
                           caller_port=request.client.port))

    return response
