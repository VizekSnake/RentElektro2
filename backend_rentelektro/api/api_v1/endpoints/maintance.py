from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from starlette.requests import Request
from starlette.responses import Response


@router.get("/metrics")
async def metrics(request: Request):
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
