from loguru import logger

from app.config import Settings
from app.repositories.sensor_repository import SensorRepositoryInterface
from app.schemas.sensor import SensorReading, SensorResponse


class SensorService:
    """Core business logic for processing IoT sensor readings.

    Responsibilities:
        - Convert Celsius temperatures to Fahrenheit
        - Emit structured alerts when temperature exceeds threshold
        - Delegate persistence to the injected repository
    """

    def __init__(
        self,
        repository: SensorRepositoryInterface,
        settings: Settings,
    ) -> None:
        self._repository = repository
        self._settings = settings

    def process_reading(self, reading: SensorReading) -> SensorResponse:
        converted_value_f: float | None = None
        alert: str | None = None

        if reading.type == "temperature":
            temp_f = self._to_fahrenheit(reading.value, reading.unit)
            converted_value_f = temp_f

            if temp_f > self._settings.TEMP_ALERT_THRESHOLD_F:
                alert = "High Temp Alert"
                logger.warning(
                    "High Temp Alert",
                    sensor_id=reading.sensor_id,
                    value_fahrenheit=temp_f,
                    original_value=reading.value,
                    original_unit=reading.unit,
                    threshold=self._settings.TEMP_ALERT_THRESHOLD_F,
                    timestamp=reading.timestamp.isoformat(),
                )

        self._repository.save(reading.model_dump())

        return SensorResponse(
            sensor_id=reading.sensor_id,
            type=reading.type,
            value=reading.value,
            unit=reading.unit,
            timestamp=reading.timestamp,
            converted_value_f=converted_value_f,
            alert=alert,
        )

    @staticmethod
    def _to_fahrenheit(value: float, unit: str) -> float:
        if unit == "celsius":
            return value * 9 / 5 + 32
        return value
