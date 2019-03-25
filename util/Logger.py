import logging

class Logger:
    def __init__(self):
        # Create the logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Time and message formatter
        logger_formatter = logging.Formatter('%(asctime)s : %(name)s - %(levelname)s - %(message)s')

        # File handler
        logger_handler = logging.FileHandler('program.log')
        logger_handler.setLevel(logging.DEBUG)
        logger_handler.setFormatter(logger_formatter)

        self.logger.addHandler(logger_handler)
    
    def log_warning(self, message):
        self.logger.warning(message)

    def log_info(self, message):
        self.logger.info(message)

    def log_debug(self, message):
        self.logger.debug(message)
    
    def log_error(self, message):
        self.logger.error(message)

    def log_critical(self, message):
        self.logger.critical(message)

if __name__ == "__main__":
    logger = Logger()
    logger.log_info("this is a test")
    logger.log_critical("this is a test")
    logger.log_warning("this is a test")
    logger.log_debug("this is a test")
    logger.log_error("this is a test")
