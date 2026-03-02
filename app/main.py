from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.config import get_settings
from app.logging_config import setup_logging
from app.routes import health, sensor


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    setup_logging(settings.LOG_LEVEL)
    logger.info("Starting {app_name} v{version}", app_name=settings.APP_NAME, version=settings.APP_VERSION)
    yield
    logger.info("Shutting down {app_name}", app_name=settings.APP_NAME)


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Production-ready IoT Sensor Ingestor API",
        lifespan=lifespan,
    )
    app.include_router(health.router)
    app.include_router(sensor.router)
    return app


app = create_app()
