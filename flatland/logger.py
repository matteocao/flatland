import logging
import os
from threading import Lock


class Logger:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Logger, cls).__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        verbose = os.getenv("VERBOSE_LOGS", "false").lower() == "true"
        self.logger = logging.getLogger("Logger")
        self.logger.propagate = False  # Prevent double logging
        self.logger.setLevel(logging.INFO if verbose else logging.CRITICAL)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("[%(levelname)s] %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message):
        self.logger.info(message)
