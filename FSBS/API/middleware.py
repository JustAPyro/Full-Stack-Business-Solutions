import datetime
import time
from fastapi import Request
from FSBS.API.dependencies import get_db
from FSBS.API.database import database_interface as dbi
from FSBS.API.structures import schemas


async def track_api(request: Request, call_next):
    dbi.submit_request(next(get_db()),
                       schemas.APIRequestCreate(
                           method=request.method,
                           endpoint=request.url.path,
                           time=datetime.datetime.now(),
                           caller_ip=request.client.host,
                           caller_port=request.client.port))
    response = await call_next(request)
    # after
    return response
