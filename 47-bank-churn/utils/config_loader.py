import yaml
import logging
from pathlib import Path

def load_config(logger: logging, path: str = "config/config.yaml") -> dict:
    """
    Load configuration from a YAML file.

    Parameters
    ----------

    logger : logging.Logger
        Logger instance used to record the analysis process, statistical results,
        and decision messages.

    path : str
        Path to the YAML configuration file.

    Returns
    -------
    dict
        Parsed configuration as a Python dictionary.

    Raises
    ------
    RuntimeError
        If the configuration file cannot be loaded.
    """

    # Convert the string path into a Path object
    config_path = Path(path)

    try:
        logger.info("Loading configuration from config.yaml")

        # Open the YAML configuration file
        with open(config_path, "r", encoding="utf-8") as f:
            # Safely parse YAML into a dictionary
            config = yaml.safe_load(f)

        logger.info("Configuration loaded successfully")

        return config

    except FileNotFoundError:
        logger.error("Configuration file not found: %s", config_path)
        raise RuntimeError(f"Configuration file not found: {config_path}")

    except yaml.YAMLError as e:
        logger.error("Error parsing YAML file: %s", e)
        raise RuntimeError(f"Error parsing YAML file: {e}")

    except Exception as e:
        logger.exception("Unexpected error while loading config")
        raise RuntimeError(f"Unexpected error while loading config: {e}")
