import os

from loguru import logger

logger.remove()
logger.add('logs/errors.log', format='{time} - {name} - {level} - {message}',
           level='ERROR', rotation='10 MB', compression='zip')
# logger.add('logs/debug.log', format='{time} - {name} - {level} - {message}',
#            level='DEBUG', rotation='10 MB', compression='zip')

LOG_DIR = 'logs'
OUTPUT_DIR = 'output'
INPUT_DIR = 'input'
DIR_NAMES = [dir_ for var_, dir_  in globals().items() if var_.endswith('_DIR')]

OUTPUT_FILENAME = 'output'
INPUT_FILENAME = 'input'

TXT_ENCODING = 'utf-8'
CSV_ENCODING = 'utf-8'
