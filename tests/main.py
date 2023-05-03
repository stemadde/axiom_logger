import os
from src.axiom_logger_stemadde.axiom_logger import AxiomHandler
import logging

logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
ah = AxiomHandler(
    os.environ.get('AXIOM_DATASET', 'test'),
    os.environ.get('AXIOM_API_TOKEN', None)
)

ah.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ah.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ah)


def main():
    print('debug')
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')


if __name__ == '__main__':
    main()
