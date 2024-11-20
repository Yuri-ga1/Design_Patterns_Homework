import os
from datetime import datetime

from src.emuns.logging_levels import LogLevel

class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self, log_file="log.log", file_level=LogLevel.INFO, console_level=LogLevel.DEBUG, enable_console=True):
        if not hasattr(self, "_initialized"):
            self.log_file = log_file
            self.file_level = file_level
            self.console_level = console_level
            self.enable_console = enable_console

            if not os.path.exists(self.log_file):
                with open(self.log_file, "w", encoding="utf-8") as _:
                    pass

            self._initialized = True
        else:
            if any([
                log_file != self.log_file,
                file_level != self.file_level,
                console_level != self.console_level,
                enable_console != self.enable_console
            ]):
                raise RuntimeError("Cannot reinitialize Logger with different parameters.")

    def _write_to_console(self, message, level):
        if self.enable_console and self._should_log(level, self.console_level):
            print(message)


    def _write_to_file(self, message, level):
        if self._should_log(level, self.file_level):
            with open(self.log_file, "a", encoding="utf-8") as file:
                file.write(message + "\n")


    def _should_log(self, level, threshold):
        levels = list(LogLevel)
        return levels.index(level) >= levels.index(threshold)


    def _format_message(self, level, message):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"{current_time} - {level.value} - {message}"


    def log(self, level: LogLevel, message: str):
        if not isinstance(level, LogLevel):
            raise ValueError(f"Invalid log level: {level}")
        formatted_message = self._format_message(level, message)
        self._write_to_console(formatted_message, level)
        self._write_to_file(formatted_message, level)


    def info(self, message: str):
        self.log(LogLevel.INFO, message)

    def warning(self, message: str):
        self.log(LogLevel.WARNING, message)

    def error(self, message: str):
        self.log(LogLevel.ERROR, message)

    def debug(self, message: str):
        self.log(LogLevel.DEBUG, message)

    def critical(self, message: str):
        self.log(LogLevel.CRITICAL, message)
