import jwt
import logging
from contextlib import asynccontextmanager
from http import HTTPStatus

import uvicorn
from fastapi import applications, FastAPI, Request, Response

from fastapi.responses import ORJSONResponse
from fastapi.openapi.docs import get_swagger_ui_html

from core.logger import setup_root_logger
from db import cache
from db.postgres import create_database, purge_database
from fastapi.responses import JSONResponse
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException

from core.config import settings
from api.v1 import notes_api, authentication
from db.redis import RedisAsyncCache
from utils.rate_limit import rate_limit


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui-bundle.min.js",
        swagger_css_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui.min.css")


applications.get_swagger_ui_html = swagger_monkey_patch


@asynccontextmanager
async def lifespan(fast_api: FastAPI):
    from models.user import User
    from models.note import Note
    from models.tag import Tag

    cache.async_cache = RedisAsyncCache()
    await create_database()
    yield

app = FastAPI(
    title='Note service',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    description='Сервис по управлению личными заметками',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


@app.middleware('http')
async def rate_limit_middleware(request: Request, call_next):
    authorization = request.headers.get('authorization')
    if not authorization:
        return await call_next(request)

    access_token = request.headers.get('authorization').split()[1]
    decoded_token = jwt.decode(access_token, options={'verify_signature': False})
    user_id = decoded_token.get('sub')
    if not rate_limit(user_id, settings.request_limit_per_minute):
        return Response(status_code=HTTPStatus.TOO_MANY_REQUESTS, content='Too Many Requests')
    return await call_next(request)


@AuthJWT.load_config
def get_config():
    return settings


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={'detail': exc.message})


app.include_router(notes_api.router, prefix='/api/v1/notes', tags=['notes'])
app.include_router(authentication.router, prefix='/api/v1/auth', tags=['auth'])

setup_root_logger()

LOGGER = logging.getLogger(__name__)
LOGGER.info('Starting App')


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_level=logging.DEBUG,
        reload=True
    )
