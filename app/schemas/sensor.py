from datetime import datetime

from pydantic import BaseModel, field_validator


class SensorReading(BaseModel):
    """Inbound sensor data from IoT devices."""

    sensor_id: str
    type: str
    value: float
    unit: str
    timestamp: datetime

    @field_validator("sensor_id")
    @classmethod
    def sensor_id_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("sensor_id must not be empty")
        return v.strip()

    @field_validator("unit")
    @classmethod
    def normalize_unit(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("type")
    @classmethod
    def normalize_type(cls, v: str) -> str:
        return v.strip().lower()


class SensorResponse(BaseModel):
    """API response after processing a sensor reading."""

    sensor_id: str
    type: str
    value: float
    unit: str
    timestamp: datetime
    converted_value_f: float | None = None
    alert: str | None = None
