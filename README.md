# IoT Sensor Ingestor API

Production-ready FastAPI service that ingests IoT sensor data, converts Celsius to Fahrenheit, and emits structured alerts for high temperature readings.

## Architecture

```
Routes (FastAPI) → Service Layer (business logic) → Repository (data persistence)
```

- **Layered Architecture** with clear separation of concerns
- **Repository Pattern** with abstract interface for swappable data backends
- **Dependency Injection** via FastAPI's `Depends()` for testability
- **Structured JSON Logging** via Loguru for observability

## Quick Start

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

## API Endpoints

### `GET /health`

Health check for deployment readiness.

```bash
curl http://localhost:8000/health
```

### `POST /sensors/data`

Ingest a sensor reading.

```bash
curl -X POST http://localhost:8000/sensors/data \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_id": "sensor-001",
    "type": "temperature",
    "value": 40.0,
    "unit": "celsius",
    "timestamp": "2026-03-01T12:00:00Z"
  }'
```

## Running Tests

```bash
source venv/bin/activate
python -m pytest tests/ -v
```

## Docker

```bash
docker build -t iot-ingestor .
docker run -p 8000:8000 iot-ingestor
```

## Configuration

All settings are configurable via environment variables with the `IOT_` prefix:

| Variable | Default | Description |
|---|---|---|
| `IOT_APP_NAME` | IoT Sensor Ingestor | Application name |
| `IOT_APP_VERSION` | 1.0.0 | Application version |
| `IOT_HOST` | 0.0.0.0 | Server host |
| `IOT_PORT` | 8000 | Server port |
| `IOT_LOG_LEVEL` | INFO | Logging level |
| `IOT_TEMP_ALERT_THRESHOLD_F` | 100.0 | Fahrenheit threshold for high temp alerts |
