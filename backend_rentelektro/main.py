from fastapi import FastAPI

from api.api_v1.endpoints import users, tools
from api.api_v1.endpoints import maintance
from core import models
from core.database import engine
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(tags="Main")
instrumentator = Instrumentator()
instrumentator.instrument(app)

models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost",
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


# app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router)
app.include_router(tools.router)
app.include_router(maintance.router)
