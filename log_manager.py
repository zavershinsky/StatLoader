# -*- coding: utf-8 -*-
import os
import logging
from logging.handlers import TimedRotatingFileHandler


class WholeIntervalRotatingFileHandler(TimedRotatingFileHandler):
    def computeRollover(self, currentTime):
        if self.when[0] == 'W' or self.when == 'MIDNIGHT':
            # use existing computation
            return super().computeRollover(currentTime)
        # round time up to nearest next multiple of the interval
        return ((currentTime // self.interval) + 1) * self.interval


class LogManager:
    # Configuration dict for the future functionality
    _levelToLevel = {1: logging.CRITICAL,
                     2: logging.ERROR,
                     3: logging.WARNING,
                     4: logging.INFO,
                     5: logging.DEBUG}

    def __init__(self, app_name: str, log_dir: str):
        self.__logger = logging.getLogger(app_name)
        self.__logger.setLevel(logging.DEBUG)
        # fh = logging.FileHandler(f'{app_name}.log')
        fh = WholeIntervalRotatingFileHandler(os.path.join(log_dir, f'{app_name}.log'), when='H', interval=1)
        fmt = logging.Formatter(f'%(asctime)s - '
                                f'%(levelname)s - '
                                f'%(name)s - '
                                # f'%(pathname)s:%(lineno)d - '
                                f'%(message)s')
        fmt.default_msec_format = '%s.%03d'
        fh.setFormatter(fmt)
        self.__logger.addHandler(fh)

    def __log(self, level, msg):
        self.__logger.log(self._levelToLevel[level], msg)

    def get_log(self):
        return self.__log

    def set_log_level(self, level: int):
        self.__logger.setLevel(self._levelToLevel[level])
