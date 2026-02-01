# logger.py
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

class LoggerConfig:
    """
    Logger configuration utility for Spark applications.
    """

    @staticmethod
    def setup_logger(name: str = "spark", level: int = logging.DEBUG, log_dir: str = "logs") -> logging.Logger:
        """
        Create and configure logger with console and file handlers.

        Parameters
        ----------
        name : str, optional
            Logger name. Default is "spark".

        level : int, optional
            Logging level. Default is logging.DEBUG.

        log_dir : str, optional
            Directory to store log files.

        Returns
        -------
        logging.Logger
            Configured logger instance.
        """

        os.makedirs(log_dir, exist_ok=True)

        # Generate log file name by date
        today = datetime.now().strftime("%Y%m%d%H%M%S")

        log_file = os.path.join(log_dir, f"{name}_{today}.log")

        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Disable log propagation to prevent duplicate logs
        logger.propagate = False

        # Remove existing handlers (avoid duplicated output)
        if logger.handlers:
            logger.handlers.clear()

        # Define log format: time | level | message
        formatter = logging.Formatter(
            fmt="{asctime} | {levelname} | {message}",
            datefmt="%Y-%m-%d %H:%M:%S",
            style="{"
        )

        # Create console handler (stdout)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)

        # # File Handler (Rotating)
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=10 * 1024 * 1024,   # 10 MB
            backupCount=10,               # Keep last 10 files
            encoding="utf-8"
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger
