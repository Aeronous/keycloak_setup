from keycloak_setup.logger import get_logger

def test_get_logger_returns_logger():
    logger = get_logger()
    assert logger.name == "keycloak_setup"
    assert logger.level == 20  # logging.INFO
    assert logger.handlers
    # Check formatter
    handler = logger.handlers[0]
    assert handler.formatter._fmt == "\u25b6\ufe0f %(levelname)s: %(message)s" 