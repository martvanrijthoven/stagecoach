import logging
from pathlib import Path
import sys


_original_stdout = sys.stdout


class StreamToLogger:
    """
    A class to redirect stdout to logging.
    """

    def __init__(self, logger, level):
        self.logger = logger
        self.level = level

    def write(self, message):
        if message.strip():  # Log only non-empty lines
            self.logger.log(self.level, message.strip())

    def flush(self):
        pass  # Needed for file-like object


def redirect_stdout_to_logger(logger):
    """
    Redirect print statements to both terminal (stdout) and log file.
    """

    class DualStream:
        def __init__(self, logger):
            self.terminal = sys.stdout
            self.logger = StreamToLogger(logger, logging.INFO)

        def write(self, message):
            # Print to terminal
            self.terminal.write(message)
            self.terminal.flush()
            # Log to the file
            self.logger.write(message)

        def flush(self):
            self.terminal.flush()

    # Redirect sys.stdout to both terminal and logger
    sys.stdout = DualStream(logger)


def setup_logging(log_path: Path):
    """
    Set up logging to only write to a log file (not to the terminal).
    """
    sys.stdout = _original_stdout

    # Create a custom logger
    logger = logging.getLogger(str(log_path))
    logger.setLevel(logging.DEBUG)  # Set the minimum logging level to DEBUG

    # Create a file handler to log messages to the file
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)  # Log everything to the file

    # Create a formatter and add it to the file handler
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Add only the file handler to the logger
    logger.addHandler(file_handler)

    # Remove any other handlers (like console/stream handlers)
    logger.handlers = [file_handler]

    redirect_stdout_to_logger(logger)
    return logger
