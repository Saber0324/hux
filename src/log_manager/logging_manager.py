import pathlib
import json
import logging
import logging.config
import logging.handlers
import atexit

ROOT = pathlib.Path(__file__).parent.parent
LOG_FILE = ROOT / "logs" / "bot.log"

logger = logging.getLogger("cogs_logger")


def setup_loggin():
    pathlib.Path(ROOT / "logs").mkdir(exist_ok=True)
    log_config_file = pathlib.Path(ROOT / "log_manager" / "logging_config.json")
    with open(log_config_file) as f:
        config = json.load(f)
    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        assert isinstance(queue_handler, logging.handlers.QueueHandler)
        if queue_handler.listener is not None:
            queue_handler.listener.start()
            atexit.register(queue_handler.listener.stop)
