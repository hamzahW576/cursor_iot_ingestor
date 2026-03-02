class SensorValidationError(Exception):
    """Raised when a sensor reading fails domain-level validation."""

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(self.detail)
