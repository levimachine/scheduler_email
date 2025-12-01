import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler('scheduler.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s  |  %(levelname)s  |  %(name)s  |  %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)



