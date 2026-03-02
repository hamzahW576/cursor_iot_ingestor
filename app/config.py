from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "IoT Sensor Ingestor"
    APP_VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    TEMP_ALERT_THRESHOLD_F: float = 100.0

    model_config = {"env_prefix": "IOT_"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
