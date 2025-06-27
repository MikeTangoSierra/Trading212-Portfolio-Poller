import logging

# Function to configure logging.
def configure_logging(log_file_name, log_level=logging.DEBUG):
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(levelname)s:%(message)s',
        handlers=[
            logging.FileHandler(log_file_name, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
