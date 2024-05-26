import sys
from contextlib import asynccontextmanager

import uvloop
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from sqlalchemy import insert, text
from starlette.middleware.cors import CORSMiddleware

from adapters.api.dataset import dataset_api
from app.containers import DependencyContainer

from adapters.api.prediction import prediction_api
from app.entity.base import BaseModel
from app.entity.dataset import DefaultDataset
from app.exceptions.http_exceptions import NotFound, ServiceException, ValidationError
from app.settings import APP_SETTINGS
from app.utils.logger import RouterLoggingMiddleware, logger
from app.utils.response import Response


class CustomFastAPI(FastAPI):
    container: DependencyContainer


@asynccontextmanager
async def lifespan(f_app: CustomFastAPI):
    async with f_app.container.db.provided.engine().begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
        _dataset = DefaultDataset(file_name="Train.csv", uuid="2ccacfe9-b825-48bb-8acf-e9b825e8bb97")

        await conn.execute(text(
            f"""INSERT INTO {DefaultDataset.__tablename__} (uuid, file_name) VALUES('{_dataset.uuid}', '{_dataset.file_name}')ON CONFLICT (uuid) DO NOTHING"""))
        await conn.commit()
        logger.info("DB Connected")

    yield


def create_app():
    origins: set = {
        "*",
        "http://localhost",
        "http://localhost:*",
    }
    _app = FastAPI(
        lifespan=lifespan,
        root_path="/ml",
        docs_url="/swagger",
    )
    _app.container = DependencyContainer()
    _app.container.wire(modules=[sys.modules[__name__]])
    _app.container.init_resources()
    _app.include_router(prediction_api,
                        tags=["Prediction"],
                        prefix=f"{APP_SETTINGS.API_V1.API_V1_PREFIX}/prediction")
    _app.include_router(
        dataset_api,
        tags=["Dataset"],
        prefix=f"{APP_SETTINGS.API_V1.API_V1_PREFIX}/dataset"
    )
    _app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.add_middleware(
        RouterLoggingMiddleware,  # type: ignore
        logger=logger,
    )
    return _app


app = create_app()

uvloop.install()


@app.exception_handler(404)
async def not_found(request, exc: HTTPException):
    if isinstance(exc.detail, dict):
        return NotFound(**exc.detail).to_response()
    return NotFound().to_response()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return ValidationError().to_response()


@app.exception_handler(500)
async def server_error_handler(request, exc):
    return ServiceException().to_response()


@app.get("/health-check")
async def health_check():
    return Response(status_code=200, message="App is up and running!")


@app.get("/swagger", include_in_schema=False)
async def swagger_ui_html() -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        init_oauth=app.swagger_ui_init_oauth,
        swagger_ui_parameters=app.swagger_ui_parameters,
        swagger_js_url="https://gcore.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://gcore.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
    )
