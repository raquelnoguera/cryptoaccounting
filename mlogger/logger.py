'''
This is standard stub code that I use for logging in all python projects.
The only variable that I customise for each project is LOGGER_FILE_NAME, but you can give it a generic name that works
for all the projects.
'''

import os
import logging
import logging.config
from pathlib import Path
LOGGER_BASE_DIR = Path(".")
LOGGER_FILE_NAME = 'cryptoaccounting.log'
LOGGER_FILE_DIR = LOGGER_BASE_DIR / 'logs'
if not LOGGER_FILE_DIR.exists():
    LOGGER_FILE_DIR.mkdir()
LOGGER_FILE_PATH = LOGGER_FILE_DIR / LOGGER_FILE_NAME
if not LOGGER_FILE_PATH.exists():
    with open(os.path.join(LOGGER_FILE_PATH), 'w') as file:
        file.write('-------------- LOGGER START --------------\n')

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "%(asctime)s %(levelname)-9s[%(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
        },
    },
    'handlers': {
        'console': {
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'formatter': 'standard',
            'filename': LOGGER_FILE_PATH,
            'class': 'logging.FileHandler',
        },

    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file']
    }
}
logging.config.dictConfig(DEFAULT_LOGGING)

def get_module_logger(mod_name):
    logger = logging.getLogger(mod_name)
    return logger
