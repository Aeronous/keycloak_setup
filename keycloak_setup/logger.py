import logging

def get_logger():
    """
    Returns a configured logger instance.
    Output format: ▶️ LEVEL: message
    """
    logger = logging.getLogger("keycloak_setup")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("\u25b6\ufe0f %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

