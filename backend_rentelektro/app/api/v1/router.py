from fastapi import APIRouter

from app.modules.rentals import endpoints as rentals
from app.modules.reviews import endpoints as reviews
from app.modules.tools import endpoints as tools
from app.modules.users import endpoints as users

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(tools.router)
api_router.include_router(rentals.router)
api_router.include_router(reviews.router)
