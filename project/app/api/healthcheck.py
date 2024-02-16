from app.config import Settings, get_settings
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/healthcheck")
async def healthcheck(settings: Settings = Depends(get_settings)):
    return {
        "responds": True,
        "environment": settings.environment,
        "testing": settings.testing,
        "client_base_url": settings.client_base_url,
        "base_url": settings.base_url,
    }
