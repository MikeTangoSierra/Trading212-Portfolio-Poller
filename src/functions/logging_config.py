import logging
import os

def configure_logging(log_filename="app.log"):
    """
    Configure logging so both Flask and subprocesses share the same log file.
    Adds both file and console output.
    """
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # ensure logs directory exists

    log_path = os.path.join(log_dir, log_filename)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(processName)s] %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ],
        force=True,  # reset existing logging setup
    )

    logging.info(f"Logging configured: {log_path}")