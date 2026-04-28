import logging
import os
from time import perf_counter

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.router import api_router
from app.core.config import settings
from app.core.database import Base, engine
from app.core.logging import setup_logging
from app.modules.maintenance import endpoints as maintenance
from app.modules.rentals import models as rentals_db  # noqa: F401
from app.modules.reviews import models as reviews_db  # noqa: F401
from app.modules.tools import models as tools_db  # noqa: F401
from app.modules.users import models as users_db  # noqa: F401

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(tags="RentElektro")
app.debug = os.getenv("DEBUG", "true").lower() == "true"
auto_create_schema = os.getenv("AUTO_CREATE_SCHEMA", "false").lower() == "true"

instrumentator = Instrumentator()
instrumentator.instrument(app)

if auto_create_schema:
    Base.metadata.create_all(bind=engine)


@app.middleware("http")
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


origins = [
    "http://localhost",
    "http://localhost:8081",
    "http://localhost:8080",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    logger.info("root_endpoint_called")
    return {"Hello": "World"}


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(maintenance.router)
