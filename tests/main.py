import os
from src.axiom_logger_stemadde.axiom_logger import AxiomHandler
import logging

logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = AxiomHandler(
    os.environ.get('dataset', 'test'),
    os.environ.get('api_token', None)
)

ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)


def main():
    print('debug')
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')


if __name__ == '__main__':
    main()
