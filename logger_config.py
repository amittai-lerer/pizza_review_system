# logger_config.py
import logging
import os # Import the os module
from logging.handlers import RotatingFileHandler

# Emojis for log levels (optional, for console output)
LOG_EMOJIS = {
    logging.DEBUG: "🐛",
    logging.INFO: "ℹ️",
    logging.WARNING: "⚠️",
    logging.ERROR: "❌",
    logging.CRITICAL: "🔥"
}

def setup_logger(name="app", log_file="logs/app.log", level=logging.INFO, max_bytes=10*1024*1024, backup_count=5):
    """Configure and return a logger with specified settings."""

    # --- Create log directory if it doesn't exist ---
    log_dir = os.path.dirname(log_file)
    # Ensure log_dir is not empty before trying to create it (e.g., if log_file is just 'app.log')
    if log_dir and not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
            print(f"Created log directory: {log_dir}") # For debugging startup
        except OSError as e:
            print(f"Error creating log directory {log_dir}: {e}")
            # Decide if you want to raise the error or fall back, e.g., to console-only logging
            # For now, we'll let it proceed, and FileHandler will fail if dir still not there.
    # --- End of new code ---

    logger = logging.getLogger(name)
    if not logger.handlers: # Avoid adding multiple handlers if called multiple times
        logger.setLevel(level)

        # Formatter
        formatter = logging.Formatter(
            f'%(asctime)s - %(levelname)-5s - {LOG_EMOJIS.get(level, "")}{name} - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # File Handler (Rotating)
        try:
            file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"Error setting up file handler for {log_file}: {e}")
            # Optionally, log to console if file logging fails
            if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)
                logger.error(f"Failed to attach file logger for {log_file}. Logging to console.")

        # Console Handler (always add for visibility, especially in Docker)
        if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

    return logger
