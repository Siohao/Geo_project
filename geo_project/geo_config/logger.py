import logging
import os

LOG_DIR = "logs"
LOG_FILE = "app.log"

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename= os.path.join(LOG_DIR, LOG_FILE),
    level= logging.INFO,
    format= "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

def get_logger(name: str):
    return logging.getLogger(name)