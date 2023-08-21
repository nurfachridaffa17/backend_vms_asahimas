import logging

class LoggingService:
    def __init__(self, app):
        self.app = app
        self.setup_logging()

    def setup_logging(self):
        # Configure logging
        logging.basicConfig(level=logging.INFO)

        # Define a handler to write logs to a file
        file_handler = logging.FileHandler('app.log')
        file_handler.setLevel(logging.INFO)

        # Define the log format
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the handler to the app's logger
        self.app.logger.addHandler(file_handler)

    def log_info(self, message):
        self.app.logger.info(message)

    def log_warning(self, message):
        self.app.logger.warning(message)

    def log_error(self, message):
        self.app.logger.error(message)