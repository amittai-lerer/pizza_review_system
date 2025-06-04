# logger_config.py
import logging

def setup_logger(name: str = "pizza-logger", log_file: str = "logs/app.log", level=logging.INFO):
    logger = logging.getLogger(name)

    if not logger.handlers:  # Prevent duplicate handlers
        logger.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
