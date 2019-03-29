import os
import logging
import datetime
from io import StringIO

from infrastructure.communication_ui.comm_ui import Communication_ui

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

        f = open(file_name, 'a+')
        f.close()

        file_handler = logging.FileHandler(file_name)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logger_formatter)

        # Stream handler for UI
        self.log_stream = StringIO() 
        self.stream_handler = logging.StreamHandler(self.log_stream)
        self.stream_handler.setLevel(logging.DEBUG)
        self.stream_handler.setFormatter(logger_formatter)

        # Add handlers to logger 
        self.logger.addHandler(file_handler)
        self.logger.addHandler(self.stream_handler)

        # Communication avec le UI

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

        #self.comm_ui = Communication_ui()
        #self.comm_ui.SendLog(self.log_stream.getvalue(), "log")
        #self.stream_handler.flush()
        #self.log_stream.seek(0)

    def log_info(self, message):
        print(message)
        self.logger.info(message)

        #self.comm_ui = Communication_ui()
        #self.comm_ui.SendLog(self.log_stream.getvalue(), "log")
        #self.stream_handler.flush()
        #self.log_stream.seek(0)

    def log_debug(self, message):
        print(message)
        self.logger.debug(message)
        
        #self.comm_ui = Communication_ui()
        #self.comm_ui.SendLog(self.log_stream.getvalue(), "log")
        #self.stream_handler.flush()
        #self.log_stream.seek(0)

    def log_error(self, message):
        print(message)
        self.logger.error(message)

        #self.comm_ui = Communication_ui()
        #self.comm_ui.SendLog(self.log_stream.getvalue(), "log")
        #self.stream_handler.flush()
        #self.log_stream.seek(0)

    def log_critical(self, message):
        print(self.log_stream.getvalue())
        self.logger.critical(message)

        #self.comm_ui = Communication_ui()
        #self.comm_ui.SendLog(self.log_stream.getvalue(), "log")
        #self.stream_handler.flush()
        #self.log_stream.seek(0)
