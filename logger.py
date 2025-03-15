from loguru import logger
import sys
from typing import Optional
from pathlib import Path
import colorama

class Logger:
    def __init__(self, log_level: str = "DEBUG", log_file: Optional[str] = "logs/app.log"):
        self.logger = logger
        self.log_level = log_level
        self.log_file = log_file
        self.setup_logger()

    def setup_logger(self):
        # Clear default handlers
        self.logger.remove()

        # Add console handler with color
        self.logger.add(
            sys.stdout,
            colorize=True,
            format=self._console_format(),
            level=self.log_level,
            enqueue=True,  # Async logging
            backtrace=True,  # Enable exception tracing
            diagnose=True   # Enable variable values in trace
        )

        # Add file handler if specified
        if self.log_file:
            log_path = Path(self.log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            self.logger.add(
                str(log_path),
                rotation="10 MB",  # Rotate logs every 10MB
                retention="5 days",  # Keep logs for 5 days
                compression="zip",
                format=self._file_format(),
                level="DEBUG",  # File logging should be most verbose
                enqueue=True,
                backtrace=True,
                diagnose=True
            )

    def _console_format(self):
        return (
            f"{colorama.Fore.GREEN}{{time:YYYY-MM-DD HH:mm:ss.SSS}}{colorama.Style.RESET_ALL} | "
            f"<level>{{level: <8}}</level> | "
            f"{colorama.Fore.CYAN}{{file}}{colorama.Style.RESET_ALL}:"
            f"{colorama.Fore.YELLOW}{{line}}{colorama.Style.RESET_ALL} - "
            f"<level>{{message}}</level>"
        )

    def _file_format(self):
        return "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {file}:{line} - {message}"

    # Proxy methods for common logging operations
    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)

    def exception(self, message: str):
        self.logger.exception(message)

    def catch(self, func=None):
        return self.logger.catch(reraise=True)(func) if func else self.logger.catch(reraise=True)

# Singleton instance pattern
singleton_logger = Logger(log_level="INFO", log_file="logs/app.log").logger

def get_logger():
    return singleton_logger
