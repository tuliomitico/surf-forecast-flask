import logging

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)
logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)