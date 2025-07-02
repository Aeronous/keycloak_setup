import yaml
import os
from keycloak_setup.logger import get_logger

logger = get_logger()

class ConfigLoader:
    """
    Loads YAML configuration file for Keycloak setup.

    Parameters:
        path (str): path to the YAML config file

    Returns:
        dict: parsed configuration data
    """

    @staticmethod
    def load_config(path: str) -> dict:
        if not os.path.isfile(path):
            logger.error(f"Configuration file '{path}' not found.")
            raise FileNotFoundError(f"Configuration file '{path}' does not exist.")
        try:
            with open(path, "r") as file:
                config = yaml.safe_load(file)
                logger.info(f"✅ Loaded configuration from '{path}'")
                return config
        except yaml.YAMLError as e:
            logger.error("❌ Invalid YAML syntax in configuration file.")
            raise e
