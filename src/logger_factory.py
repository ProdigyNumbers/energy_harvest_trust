import logging


class LoggerFactory:
    def __init__(self, name: str):
        self.name = name

    def get_logger(self):

        # Create logger
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        # # 'application code'
        # logger.debug('debug message')
        # logger.info('info message')
        # logger.warning('warn message')
        # logger.error('error message')
        # logger.critical('critical message')

        return logger
