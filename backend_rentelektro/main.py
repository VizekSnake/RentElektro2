from fastapi import FastAPI

from api.api_v1.endpoints import users, tools, rentals, reviews
from api.api_v1.endpoints import maintance
from core import models
from core.database import engine
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.middleware.cors import CORSMiddleware

from core.mongodb import db as mongo_db

app = FastAPI(tags="Main", root_path="/api")
instrumentator = Instrumentator()
instrumentator.instrument(app)

models.Base.metadata.create_all(bind=engine)

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
    return {"Hello": "World"}


# app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router)
app.include_router(tools.router)
app.include_router(rentals.router)
app.include_router(maintance.router)
app.include_router(reviews.router)
