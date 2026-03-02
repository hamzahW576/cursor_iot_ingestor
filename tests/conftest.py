import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.repositories.sensor_repository import InMemorySensorRepository
from app.routes.sensor import get_repository, get_sensor_service
from app.services.sensor_service import SensorService


@pytest.fixture
def settings() -> Settings:
    return Settings()


@pytest.fixture
def repository() -> InMemorySensorRepository:
    return InMemorySensorRepository()


@pytest.fixture
def sensor_service(repository, settings) -> SensorService:
    return SensorService(repository=repository, settings=settings)


@pytest.fixture
def client(repository) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_repository] = lambda: repository
    yield TestClient(app)
    app.dependency_overrides.clear()
