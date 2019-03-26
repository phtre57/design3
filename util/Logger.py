import os
import logging
import datetime


class Logger(object):
    def __init__(self, module_name):
        # File paths from root
        self.sequence_count_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "sequence_count.txt"))
        self.log_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "log/sequenceX.log"))

        # Create the logger
        self.logger = logging.getLogger(module_name)
        self.logger.setLevel(logging.DEBUG)

        # Time and message formatter
        logger_formatter = logging.Formatter(
            '%(asctime)s : %(name)s \n%(levelname)s - %(message)s')

        # File handler
        file_number = open(self.sequence_count_path).read()
        file_name = self.log_path.replace("X", file_number)

        # File Check
        f = open(file_name, 'a+')
        f.close()

        logger_handler = logging.FileHandler(file_name)
        logger_handler.setLevel(logging.DEBUG)
        logger_handler.setFormatter(logger_formatter)

        self.logger.addHandler(logger_handler)

    def increment_sequence_number(self):
        file_number = open(self.sequence_count_path).read()

        new_file_number = int(file_number) + 1
        new_file_number = str(new_file_number)

        f = open(self.sequence_count_path, 'w')
        f.write(new_file_number)
        f.close()

    def reset_sequence_number(self):
        f = open(self.sequence_count_path, 'w')
        f.write(str(1))
        f.close()

    def log_warning(self, message):
        print(message)
        self.logger.warning(message)

    def log_info(self, message):
        print(message)
        self.logger.info(message)

    def log_debug(self, message):
        print(message)
        self.logger.debug(message)

    def log_error(self, message):
        print(message)
        self.logger.error(message)

    def log_critical(self, message):
        print(message)
        self.logger.critical(message)
