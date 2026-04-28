import logging
from time import perf_counter

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.modules.maintenance import endpoints as maintenance

setup_logging()
logger = logging.getLogger(__name__)
settings = get_settings()


async def log_requests(request: Request, call_next):
    started = perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        duration_ms = (perf_counter() - started) * 1000
        logger.exception(
            "request_failed method=%s path=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise

    duration_ms = (perf_counter() - started) * 1000
    logger.info(
        "request method=%s path=%s status=%s duration_ms=%.2f",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


def configure_middlewares(app: FastAPI) -> None:
    app.middleware("http")(log_requests)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["*"],
    )
    Instrumentator().instrument(app)


def configure_routes(app: FastAPI) -> None:
    app.add_api_route("/", read_root, methods=["GET"], response_class=PlainTextResponse)
    app.include_router(api_router, prefix=settings.API_V1_STR)
    app.include_router(maintenance.router)


def read_root() -> str:
    logger.info("root_endpoint_called")
    return r"""
 ____            _   _____ _           _             
|  _ \ ___ _ __ | |_| ____| | ___  ___| |_ _ __ ___  
| |_) / _ \ '_ \| __|  _| | |/ _ \/ __| __| '__/ _ \ 
|  _ <  __/ | | | |_| |___| |  __/ (__| |_| | | (_) |
|_| \_\___|_| |_|\__|_____|_|\___|\___|\__|_|  \___/ 

API v1
Go for swagger: host_url/docs 
""".strip()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG, tags=["RentElektro"])
    configure_middlewares(app)
    configure_routes(app)

    return app


app = create_app()
