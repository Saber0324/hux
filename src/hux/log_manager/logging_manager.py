import pathlib
import json
import logging
import logging.config
import logging.handlers
import atexit

ROOT = pathlib.Path(__file__).parent.parent
LOG_DIR = ROOT / "logs"
CONFIG_JSON = ROOT / "log_manager" / "logging_config.json"
logger = logging.getLogger("cogs_logger")


def setup_loggin():
    pathlib.Path(ROOT / "logs").mkdir(exist_ok=True)
    log_config_file = CONFIG_JSON
    with open(log_config_file) as f:
        config = json.load(f)
    LOG_DIR.mkdir(exist_ok=True)
    config["handlers"]["file"]["filename"] = str(LOG_DIR / "bot.log")
    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        assert isinstance(queue_handler, logging.handlers.QueueHandler)
        if queue_handler.listener is not None:
            queue_handler.listener.start()
            atexit.register(queue_handler.listener.stop)
