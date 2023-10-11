import logging
from flask.logging import default_handler
import os

from logging.handlers import RotatingFileHandler
from logging import StreamHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_PATH = os.path.join(BASE_DIR, 'logs')

LOG_PATH_INFO = os.path.join(LOG_PATH, 'info.log')
LOG_PATH_WARNING = os.path.join(LOG_PATH, 'warn.log')
LOG_PATH_ERROR = os.path.join(LOG_PATH, 'error.log')
LOG_PATH_CRITICAL = os.path.join(LOG_PATH, 'critical.log')
# log file max size 100MB
LOG_FILE_MAX_BYTES = 100 * 1024 * 1024
LOG_FILE_BACKUP_COUNT = 10


class Logger(object):

    def init_app(self, app):
        # remove default handler
        app.logger.removeHandler(default_handler)
        formatter = logging.Formatter(
            '%(asctime)s [%(thread)d:%(threadName)s] [%(filename)s:%(module)s:%(funcName)s] '
            '[%(levelname)s]: %(message)s'
        )

        # input INFO log
        file_handler = RotatingFileHandler(
            filename=LOG_PATH_INFO,
            mode='a',
            maxBytes=LOG_FILE_MAX_BYTES,
            backupCount=LOG_FILE_BACKUP_COUNT,
            encoding='utf-8'
        )

        file_handler.setFormatter(formatter)
        stream_handler = StreamHandler()
        stream_handler.setFormatter(formatter)
        info_filter = logging.Filter()
        info_filter.filter = lambda record: record.levelno < logging.WARNING  # set filter
        err_filter = logging.Filter()
        err_filter.filter = lambda record: record.levelno >= logging.INFO
        stream_handler.addFilter(err_filter)
        file_handler.addFilter(info_filter)

        for logger in (
                # add more log module
                app.logger,
                logging.getLogger('sqlalchemy'),
                logging.getLogger('werkzeug')
        ):
            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)


        # input WARNING  log
        file_handler2 = RotatingFileHandler(
            filename=LOG_PATH_WARNING,
            mode='a',
            maxBytes=LOG_FILE_MAX_BYTES,
            backupCount=LOG_FILE_BACKUP_COUNT,
            encoding='utf-8'
        )

        file_handler2.setFormatter(formatter)
        file_handler2.setLevel(logging.WARNING)
        info_filter2 = logging.Filter()
        info_filter2.filter = lambda record: record.levelno < logging.ERROR  # set filter
        file_handler2.addFilter(info_filter2)

        for logger in (
                # add more log module
                app.logger,
                logging.getLogger('sqlalchemy'),
                logging.getLogger('werkzeug')

        ):
            logger.addHandler(file_handler2)


        # input ERROR log
        file_handler3 = RotatingFileHandler(
            filename=LOG_PATH_ERROR,
            mode='a',
            maxBytes=LOG_FILE_MAX_BYTES,
            backupCount=LOG_FILE_BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler3.setFormatter(formatter)
        file_handler3.setLevel(logging.ERROR)
        info_filter3 = logging.Filter()
        info_filter3.filter = lambda record: record.levelno < logging.CRITICAL  # set filter
        file_handler3.addFilter(info_filter3)
        for logger in (
                    # add more log module
                app.logger,
                logging.getLogger('sqlalchemy'),
                logging.getLogger('werkzeug')
            ):
            logger.addHandler(file_handler3)


        # input CRITICAL log
        file_handler4 = RotatingFileHandler(
            filename=LOG_PATH_CRITICAL,
            mode='a',
            maxBytes=LOG_FILE_MAX_BYTES,
            backupCount=LOG_FILE_BACKUP_COUNT,
            encoding='utf-8'
        )

        file_handler4.setFormatter(formatter)
        file_handler4.setLevel(logging.CRITICAL)

        for logger in (
                # add more log module
                app.logger,
                logging.getLogger('sqlalchemy'),
                logging.getLogger('werkzeug')
        ):
            logger.addHandler(file_handler4)
