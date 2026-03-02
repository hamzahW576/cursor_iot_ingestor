from datetime import datetime, timezone

from app.schemas.sensor import SensorReading


def _make_reading(**overrides) -> SensorReading:
    defaults = {
        "sensor_id": "sensor-001",
        "type": "temperature",
        "value": 37.0,
        "unit": "celsius",
        "timestamp": datetime(2026, 3, 1, 12, 0, 0, tzinfo=timezone.utc),
    }
    defaults.update(overrides)
    return SensorReading(**defaults)


class TestCelsiusToFahrenheitConversion:
    def test_converts_celsius_to_fahrenheit(self, sensor_service):
        reading = _make_reading(value=0.0, unit="celsius")
        response = sensor_service.process_reading(reading)
        assert response.converted_value_f == 32.0

    def test_body_temp_conversion(self, sensor_service):
        reading = _make_reading(value=37.0, unit="celsius")
        response = sensor_service.process_reading(reading)
        assert response.converted_value_f == pytest.approx(98.6)

    def test_no_conversion_for_fahrenheit_unit(self, sensor_service):
        reading = _make_reading(value=98.6, unit="fahrenheit")
        response = sensor_service.process_reading(reading)
        assert response.converted_value_f == 98.6

    def test_boiling_point_conversion(self, sensor_service):
        reading = _make_reading(value=100.0, unit="celsius")
        response = sensor_service.process_reading(reading)
        assert response.converted_value_f == 212.0


class TestHighTempAlert:
    def test_alert_triggered_above_threshold(self, sensor_service):
        reading = _make_reading(value=40.0, unit="celsius")  # 104°F
        response = sensor_service.process_reading(reading)
        assert response.alert == "High Temp Alert"

    def test_no_alert_at_threshold(self, sensor_service):
        reading = _make_reading(value=100.0, unit="fahrenheit")  # exactly 100°F
        response = sensor_service.process_reading(reading)
        assert response.alert is None

    def test_no_alert_below_threshold(self, sensor_service):
        reading = _make_reading(value=30.0, unit="celsius")  # 86°F
        response = sensor_service.process_reading(reading)
        assert response.alert is None


class TestNonTemperatureSensor:
    def test_humidity_sensor_no_conversion(self, sensor_service):
        reading = _make_reading(type="humidity", value=65.0, unit="percent")
        response = sensor_service.process_reading(reading)
        assert response.converted_value_f is None
        assert response.alert is None

    def test_pressure_sensor_no_conversion(self, sensor_service):
        reading = _make_reading(type="pressure", value=1013.25, unit="hpa")
        response = sensor_service.process_reading(reading)
        assert response.converted_value_f is None
        assert response.alert is None


class TestPersistence:
    def test_reading_saved_to_repository(self, sensor_service, repository):
        reading = _make_reading()
        sensor_service.process_reading(reading)
        stored = repository.get_all()
        assert len(stored) == 1
        assert stored[0]["sensor_id"] == "sensor-001"

    def test_multiple_readings_persisted(self, sensor_service, repository):
        sensor_service.process_reading(_make_reading(sensor_id="s1"))
        sensor_service.process_reading(_make_reading(sensor_id="s2"))
        assert len(repository.get_all()) == 2


import pytest
