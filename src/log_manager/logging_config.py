import json

from log_manager.logging_manager import LOG_FILE

loggin_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s %(asctime)s: %(message)s",
        },
        "detailed": {
            "format": "[%(levelname)s | %(module)s | L%(lineno)d] %(asctime)s: %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "stderr": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": "ext://sys.stderr",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "filename": str(LOG_FILE),
            "maxBytes": 32 * 1024 * 1024,
            "backupCount": 3,
        },
        "queue_handler": {
            "class": "logging.handlers.QueueHandler",
            "handlers": ["stderr", "file"],
            "respect_handler_level": True,
        },
    },
    "loggers": {
        "root": {"level": "DEBUG", "handlers": ["queue_handler"]},
        "discord": {"level": "WARNING", "propagate": False},
        "aiosqlite": {"level": "WARNING", "propagate": False},
    },
}

with open("log_manager/logging_config.json", "w") as f:
    json.dump(loggin_config, f, indent=True)
