LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # let Uvicorn logs stay
    "formatters": {
        "default": {
            "format": "%(asctime)s - [%(name)s] - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "default",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

