import logging


def monitor_logger(
        log_file=None,
        log_name=__name__,
        log_level=logging.DEBUG,
        mode='w',
        log_to_console=True):

    # create logger
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s | %(message)s')

    if log_to_console is True:
        # create console handler
        handler = logging.StreamHandler()
        # set handler log level
        handler.setLevel(log_level)
        # set handler formatter
        handler.setFormatter(formatter)
        # add handler to logger
        logger.addHandler(handler)

    if log_file is True:
        # create log_file handler
        handler = logging.FileHandler(log_file, mode)
        # set handler log level
        handler.setLevel(log_level)
        # set handler formatter
        handler.setFormatter(formatter)
        # add handler to logger
        logger.addHandler(handler)
    return logger
