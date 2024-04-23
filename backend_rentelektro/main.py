from fastapi import FastAPI

from api.api_v1.endpoints import users, tools
from api.api_v1.endpoints import maintance
from core import models
from core.database import engine
# from api.routers import auth
from starlette.staticfiles import StaticFiles
from starlette.responses import Response
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.requests import Request
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import JSONResponse
app = FastAPI()
instrumentator = Instrumentator()
# Instrument the FastAPI app
instrumentator.instrument(app)

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}


# app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router)
app.include_router(tools.router)
app.include_router(maintance.router)
