import logging

from django.conf import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[])

HANDLERS = getattr(settings, "DRF_LOGGER_HANDLER", [])
LOGGING_FILE = getattr(settings, "DRF_LOGGER_FILE", "/tmp/rest_logger.log")

if "file" in HANDLERS:
    logger.addHandler(logging.FileHandler(filename=LOGGING_FILE))

if "console" in HANDLERS:
    logger.addHandler(logging.StreamHandler())
