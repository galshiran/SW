from os.path import abspath, join, dirname
import sys
import logging


logging.getLogger('werkzeug').disabled = True

# Set logger configuration
logger_file_name = "results.txt"
logger_dir = dirname(abspath(sys.modules['__main__'].__file__))
logger_file_path = join(logger_dir, logger_file_name)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler(logger_file_path, 'w', 'utf-8')
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler)