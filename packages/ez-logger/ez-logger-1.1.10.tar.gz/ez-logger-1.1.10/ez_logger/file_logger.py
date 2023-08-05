import logging
import logging.handlers
import colorlog
import os
import uuid
from ez_logger.base_logger import BaseLogger
from ez_logger.console_logger import ConsoleLogger


class FileLogger(BaseLogger):
    """
    FileLogger provides a logger that could be used for batch processing applications.
    It uses colorlog formatter to color code log messages for different log levels.

    Parameters
    ----------
    name : `string`, `optional`
         Name of the logger.
    log_level : `string`, `optional`
         log_level
         Default value is info. Other allowed values are debug, warning, error or critical
    console_logging : `bool`, `optional`
         Should log messages be shown on the console?
         Default is True
    log_file : `string`, `optional`
         If not specified, then it will use a file_name { name }.log. If name is none then the log file will be app.log
    log_dir : `string`, `optional`
         The directory where the log_file is created. If not specified, then log_file will be created in the current directory.
         If directory does not exist, or the user does not have write permission, then log_file will be created in current directory.
    Examples
    --------
    >>> logger = FileLogger(log_file='test.log', log_dir='/tmp')
    >>> logger.info(message='process started')
    """

    def __init__(self, console_logging=True, log_level='info', name=None, log_file=None,
                 log_dir=None):
        super(FileLogger, self).__init__(
            name=name,
            log_level=log_level
        )
        self.console_logging = console_logging
        self.log_file = log_file
        self.log_dir = log_dir

        # set the logger
        self.logger = self.__getLogger()

    def __check_dir(self, dir_path):
        dummypath = os.path.join(dir_path, str(uuid.uuid4()))
        try:
            with open(dummypath, 'w'):
                pass
            os.remove(dummypath)
            return True
        except IOError:
            return False

    def __getLogfile(self):
        # set log_file
        if self.log_file is None:
            if self.name is None:
                self.log_file = 'app.log'
            else:
                self.log_file = '{0}.log'.format(self.name)

        if not self.log_dir:
            logfile = self.log_file
        else:
            # checking if the self.log_dir exists or has write access.
            if self.__check_dir(self.log_dir):
                logfile = '{0}/{1}'.format(self.log_dir, self.log_file)
            else:
                logfile = self.log_file
                # if self.log_dir does not exist or has write access.
                # then display a console warning.
                console_logger = ConsoleLogger()
                console_logger.warning(
                    'Log directory {0} does not exist or user does not have write permission. '
                    'So creating the log file in the local directory.'.format(self.log_dir)
                )
        return logfile

    def _get_file_formatter(self):
        """
        _get_file_formatter indicates how the log file record should be formatted
        It can be overridden by the child class
        :return:
        """
        return '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    def __get_file_handler(self):
        """
        __get_file_handler creates the RotatingFileHandler.
        """
        file_handler = logging.handlers.RotatingFileHandler(
            self.__getLogfile(),
            maxBytes=5 * 1024 * 1024,
            backupCount=2
        )
        file_formatter = colorlog.ColoredFormatter(
            self._get_file_formatter()
        )
        file_handler.setFormatter(file_formatter)
        return file_handler

    def __getLogger(self):
        # Create a logger object
        logger = logging.getLogger(
            name=self._get_logger_name()
        )

        # Set the log level
        logger.setLevel(self._get_log_level())

        # Remove if any loggers already exist. Logger is a singleton, so even if separate logger
        # are created, the handlers get appended.
        while len(logger.handlers) > 0:
            logger.handlers.pop()

        # Add file handler
        logger.addHandler(self.__get_file_handler())

        # Add console handler, if needed
        if self.console_logging:
            logger.addHandler(self._get_console_handler())
        return logger
