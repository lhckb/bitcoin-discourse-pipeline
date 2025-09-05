import logging
from rich.logging import RichHandler

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            RichHandler()
        ]
    )

    return logging.getLogger("bitcoin_discourse_pipeline")