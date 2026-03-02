import sys

from loguru import logger


def setup_logging(log_level: str = "INFO") -> None:
    """Configure Loguru for structured JSON logging to stdout.

    Removes the default pretty-print handler and replaces it with a
    JSON-serialized sink — required for DigitalOcean App Platform and
    any log aggregator (Datadog, Loki, CloudWatch, etc.).
    """
    logger.remove()
    logger.add(
        sys.stdout,
        level=log_level.upper(),
        serialize=True,
    )
