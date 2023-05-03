import os
import time
from src.axiom_logger import AxiomHandler
import logging

logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
ah = AxiomHandler(
    os.environ.get('AXIOM_DATASET', 'test'),
    os.environ.get('AXIOM_API_TOKEN', None),
    mode='log_count',
    log_count=5
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
    print('logged debug')
    logger.info('info message')
    print('logged info')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')
    time.sleep(10)
    logger.critical('test sleep message')
    print('logged critical test')


if __name__ == '__main__':
    main()
