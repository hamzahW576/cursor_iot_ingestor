from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.config import Settings, get_settings
from app.exceptions.sensor_exceptions import SensorValidationError
from app.repositories.sensor_repository import (
    InMemorySensorRepository,
    SensorRepositoryInterface,
)
from app.schemas.sensor import SensorReading, SensorResponse
from app.services.sensor_service import SensorService

router = APIRouter(prefix="/sensors", tags=["Sensors"])

_repository = InMemorySensorRepository()


def get_repository() -> SensorRepositoryInterface:
    return _repository


def get_sensor_service(
    repository: SensorRepositoryInterface = Depends(get_repository),
    settings: Settings = Depends(get_settings),
) -> SensorService:
    return SensorService(repository=repository, settings=settings)


@router.post(
    "/data",
    response_model=SensorResponse,
    status_code=status.HTTP_201_CREATED,
)
def ingest_sensor_data(
    reading: SensorReading,
    service: SensorService = Depends(get_sensor_service),
) -> SensorResponse:
    try:
        return service.process_reading(reading)
    except SensorValidationError as exc:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.detail},
        )
