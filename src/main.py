import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import applications, FastAPI, Request

from fastapi.responses import ORJSONResponse
from fastapi.openapi.docs import get_swagger_ui_html

from db.postgres import create_database, purge_database
from fastapi.responses import JSONResponse
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException

from core.config import settings
from api.v1 import notes_api


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui-bundle.min.js",
        swagger_css_url="https://cdn.staticfile.net/swagger-ui/5.1.0/swagger-ui.min.css")


applications.get_swagger_ui_html = swagger_monkey_patch


@asynccontextmanager
async def lifespan(fast_api: FastAPI):
    await create_database()
    yield

app = FastAPI(
    title='Note service',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


@AuthJWT.load_config
def get_config():
    return settings


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(notes_api.router, prefix='/api/v1/notes', tags=['notes'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_level=logging.DEBUG,
        reload=True
    )
