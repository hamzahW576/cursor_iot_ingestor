from fastapi import APIRouter, Depends

from app.config import Settings, get_settings

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check(settings: Settings = Depends(get_settings)) -> dict:
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
