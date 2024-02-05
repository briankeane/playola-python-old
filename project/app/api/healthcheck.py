from fastapi import APIRouter, Depends

from app.config import get_settings, Settings

router = APIRouter()


@router.get("/healthcheck")
async def healthcheck(settings: Settings = Depends(get_settings)):
    return {
        "responds": True,
        "environment": settings.environment,
        "testing": settings.testing
    }