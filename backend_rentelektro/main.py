import os

from core.database import engine
from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from maintance import endpoints as maintance
from prometheus_fastapi_instrumentator import Instrumentator
from rentals import endpoints as rentals
from rentals import models as rentals_db
from reviews import endpoints as reviews
from reviews import models as reviews_db
from tools import endpoints as tools
from tools import models as tools_db
from users import endpoints as users
from users import models as users_db

app = FastAPI(tags="RentElektro", root_path="/api")
app.debug = os.getenv("DEBUG", "true").lower() == "true"

app.add_middleware(
    DebugToolbarMiddleware,
    panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"],
)

instrumentator = Instrumentator()
instrumentator.instrument(app)

users_db.Base.metadata.create_all(bind=engine)
tools_db.Base.metadata.create_all(bind=engine)
rentals_db.Base.metadata.create_all(bind=engine)
reviews_db.Base.metadata.create_all(bind=engine)



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
