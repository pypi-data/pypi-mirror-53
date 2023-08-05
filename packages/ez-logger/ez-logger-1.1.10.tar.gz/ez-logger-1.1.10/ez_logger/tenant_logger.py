import logging
import logging.handlers
import colorlog
import os
import uuid
from ez_logger.file_logger import FileLogger
from ez_logger.console_logger import ConsoleLogger


class TenantLogger(FileLogger):
    """
    TenantLogger is a file logger that can be used when the application uses a single log file for processing multiple clients.
    It descends from FileFormatter and overrides the formatter, log, warn, debug, critical methods

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
    >>> logger = TenantLogger(log_file='multi-tenant.log', log_dir='/tmp')
    >>> logger.info(message='Process started', tenant='tenant1')
    """

    def __init__(self, console_logging=True, log_level='info', name=None, log_file=None,
                 log_dir=None):
        super(TenantLogger, self).__init__(
            name=name,
            log_level=log_level,
            console_logging=console_logging,
            log_file=log_file,
            log_dir=log_dir
        )

    def _get_file_formatter(self):
        return '%(log_color)s%(asctime)s - %(name)s - %(tenant)s - %(levelname)s - %(message)s'

    def info(self, message, tenant=None):
        """
        Writes info messages, these messages will only be written if
        log_level is set to debug or info.
        Formatter will use the tenant name in the log record.
        """
        self.logger.info(message, extra={'tenant': tenant})

    def error(self, message, tenant=None):
        """
        Writes error messages, these messages will only be written if
        log_level is set to debug, info, warning or error.
        Formatter will use the tenant name in the log record.
        """
        self.logger.error(message, extra={'tenant': tenant})

    def warning(self, message, tenant=None):
        """
        Writes warning messages, these messages will only be written
        if log_level is set to debug, info or warning.
        Formatter will use the tenant name in the log record.
        """
        self.logger.warning(message, extra={'tenant': tenant})

    def critical(self, message, tenant=None):
        """
        Writes error messages, these messages will be written
        regardless of the log_level (it could be set to debug,
        info, warning, error or critical).
        Formatter will use the tenant name in the log record.
        """
        self.logger.critical(message, extra={'tenant': tenant})

    def debug(self, message, tenant=None):
        """
        Writes debug messages, these messages will only be written
        if log_level is set to debug.
        Formatter will use the tenant name in the log record.
        """
        self.logger.debug(message, extra={'tenant': tenant})
