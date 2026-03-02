from abc import ABC, abstractmethod


class SensorRepositoryInterface(ABC):
    """Abstract contract for sensor data persistence.

    Any concrete repository (in-memory, PostgreSQL, TimescaleDB, etc.)
    must implement these methods. The service layer depends only on this
    interface, never on a concrete implementation.
    """

    @abstractmethod
    def save(self, reading: dict) -> dict:
        ...

    @abstractmethod
    def get_all(self) -> list[dict]:
        ...


class InMemorySensorRepository(SensorRepositoryInterface):
    """List-backed repository for development and testing.

    Not suitable for production workloads — data is lost on restart
    and access is not thread-safe. Swap with a database-backed
    implementation for production use.
    """

    def __init__(self) -> None:
        self._store: list[dict] = []

    def save(self, reading: dict) -> dict:
        self._store.append(reading)
        return reading

    def get_all(self) -> list[dict]:
        return list(self._store)
