import logging

def get_logger(file_name:str):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(file_name, encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s  |  %(levelname)s  |  %(name)s  |  %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

