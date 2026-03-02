VALID_PAYLOAD = {
    "sensor_id": "sensor-001",
    "type": "temperature",
    "value": 40.0,
    "unit": "celsius",
    "timestamp": "2026-03-01T12:00:00Z",
}


class TestPostSensorData:
    def test_successful_ingestion(self, client):
        response = client.post("/sensors/data", json=VALID_PAYLOAD)
        assert response.status_code == 201
        body = response.json()
        assert body["sensor_id"] == "sensor-001"
        assert body["converted_value_f"] == 104.0
        assert body["alert"] == "High Temp Alert"

    def test_celsius_below_threshold(self, client):
        payload = {**VALID_PAYLOAD, "value": 30.0}
        response = client.post("/sensors/data", json=payload)
        assert response.status_code == 201
        assert response.json()["alert"] is None

    def test_missing_required_field(self, client):
        payload = {"sensor_id": "sensor-001", "type": "temperature"}
        response = client.post("/sensors/data", json=payload)
        assert response.status_code == 422

    def test_empty_sensor_id_rejected(self, client):
        payload = {**VALID_PAYLOAD, "sensor_id": "   "}
        response = client.post("/sensors/data", json=payload)
        assert response.status_code == 422

    def test_humidity_sensor_no_alert(self, client):
        payload = {**VALID_PAYLOAD, "type": "humidity", "value": 85.0, "unit": "percent"}
        response = client.post("/sensors/data", json=payload)
        assert response.status_code == 201
        body = response.json()
        assert body["converted_value_f"] is None
        assert body["alert"] is None
