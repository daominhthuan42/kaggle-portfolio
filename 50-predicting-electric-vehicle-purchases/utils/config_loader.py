# config_loader.py
import yaml
import logging
from pathlib import Path

# Project Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "config" / "config.yaml"

# Configuration Loader
def load_config(logger: logging.Logger, path: str | Path = CONFIG_PATH) -> dict:
    """
    Load configuration from a YAML file and resolve project paths.

    Parameters
    ----------
    logger : logging.Logger
        Logger instance used to record the configuration loading process.

    path : str or Path
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

    # Convert the configuration path into a Path object
    config_path = Path(path)

    try:
        logger.info("Loading configuration from %s", config_path.name)

        # Open the YAML configuration file
        with open(config_path, "r", encoding="utf-8") as f:
            # Safely parse YAML into a dictionary
            config = yaml.safe_load(f)

        # Validate YAML content
        if not isinstance(config, dict):
            raise ValueError("Configuration file must contain a valid YAML mapping.")
        
        # Resolve Project Paths
        dataset_paths = config.get("dataset", {}).get("paths", {})

        for key, relative_path in dataset_paths.items():
            if relative_path is None:
                continue
            dataset_paths[key] = str((ROOT_DIR / relative_path).resolve())

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
