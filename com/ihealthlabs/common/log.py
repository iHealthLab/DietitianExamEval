import logging
import os
import re
from logging.handlers import TimedRotatingFileHandler


class Log:

    def __init__(self, name=None):
        self.path = 'log'
        if name:
            self.path = os.path.join(self.path, name)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        self.formatter = logging.Formatter(
            '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
        if not self.logger.handlers:
            self.logger.propagate = 0
            fh = TimedRotatingFileHandler(
                filename=os.path.join(self.path, 'debug'), when="MIDNIGHT", interval=1, backupCount=30
            )
            fh.suffix = "%Y-%m-%d.log"
            fh.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(self.formatter)
            self.logger.addHandler(fh)

            err_fh = TimedRotatingFileHandler(
                filename=os.path.join(self.path, 'error'), when="MIDNIGHT", interval=1, backupCount=30
            )
            err_fh.suffix = "%Y-%m-%d.log"
            err_fh.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
            err_fh.setLevel(logging.ERROR)
            err_fh.setFormatter(self.formatter)
            self.logger.addHandler(err_fh)

            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(self.formatter)
            self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger
