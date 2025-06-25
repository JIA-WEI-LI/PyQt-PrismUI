import logging
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR, "prism_ui.log")

DEBUG_MODE = True
ENABLE_FILE_LOG = True

LOG_FORMAT = '[%(asctime)s][%(levelname)s] %(name)s:%(lineno)d → %(message)s'
formatter = logging.Formatter(LOG_FORMAT)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG if DEBUG_MODE else logging.INFO)

file_handler = None
if ENABLE_FILE_LOG:
    file_handler = logging.FileHandler(LOG_FILE_PATH, mode='w', encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG if DEBUG_MODE else logging.INFO)

if not any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers):
    root_logger.addHandler(console_handler)
if file_handler and not any(isinstance(h, logging.FileHandler) for h in root_logger.handlers):
    root_logger.addHandler(file_handler)

module_levels = {
    "prism_ui.tools.icon_resource_generator": logging.DEBUG,
}

for mod, level in module_levels.items():
    logging.getLogger(mod).setLevel(level)