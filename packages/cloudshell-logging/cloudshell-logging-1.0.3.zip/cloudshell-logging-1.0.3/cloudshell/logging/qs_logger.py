#!/usr/bin/python
import logging
import os
import re
import sys
import threading
import time
import traceback
from datetime import datetime
from functools import wraps
from logging import StreamHandler

from cloudshell.logging.interprocess_logger import MultiProcessingLog
from cloudshell.logging.qs_config_parser import QSConfigParser

# Logging Levels
LOG_LEVELS = {
    "INFO": logging.INFO,
    "WARN": logging.WARN,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
    "FATAL": logging.FATAL,
    "DEBUG": logging.DEBUG,
}

# default settings
DEFAULT_FORMAT = (
    "%(asctime)s [%(levelname)s]: %(name)s %(module)s - %(funcName)-20s %(message)s"
)
DEFAULT_TIME_FORMAT = "%Y%m%d%H%M%S"
DEFAULT_LEVEL = "INFO"
LOG_SECTION = "Logging"
WINDOWS_OS_FAMILY = "nt"

_LOGGER_CONTAINER = {}
_LOGGER_LOCK = threading.Lock()


def get_settings():
    """Read configuration settings from config or use DEFAULTS.

    :return: config obj
    """
    config = {}
    # Level
    log_level = QSConfigParser.get_setting(LOG_SECTION, "LOG_LEVEL") or DEFAULT_LEVEL
    config["LOG_LEVEL"] = log_level

    # Log format
    log_format = QSConfigParser.get_setting(LOG_SECTION, "LOG_FORMAT") or DEFAULT_FORMAT
    config["FORMAT"] = log_format

    # UNIX log path
    config["UNIX_LOG_PATH"] = QSConfigParser.get_setting(LOG_SECTION, "UNIX_LOG_PATH")

    # Windows log path
    config["WINDOWS_LOG_PATH"] = QSConfigParser.get_setting(
        LOG_SECTION, "WINDOWS_LOG_PATH"
    )

    # Default log path for all systems
    config["DEFAULT_LOG_PATH"] = QSConfigParser.get_setting(
        LOG_SECTION, "DEFAULT_LOG_PATH"
    )

    # Time format
    time_format = (
        QSConfigParser.get_setting(LOG_SECTION, "TIME_FORMAT") or DEFAULT_TIME_FORMAT
    )
    config["TIME_FORMAT"] = time_format

    return config


def _get_log_path_config(config):
    """Get log path based on the environment variable or Windows/Unix config setting.

    :param dict[str] config:
    :rtype: str
    """
    if "LOG_PATH" in os.environ:
        return os.environ["LOG_PATH"]

    if os.name == WINDOWS_OS_FAMILY:
        tpl = config.get("WINDOWS_LOG_PATH")
        if tpl:
            try:
                return tpl.format(**os.environ)
            except KeyError:
                print(  # noqa: T001
                    "Environment variable is not defined in the template {}".format(tpl)
                )
    else:
        return config.get("UNIX_LOG_PATH")


def _prepare_log_path(log_path, log_file_name):
    """Create logs directory if needed and return full path to the log file.

    :param str log_path:
    :param str log_file_name:
    :rtype: str
    """
    if log_path.startswith(".."):
        log_path = os.path.join(os.path.dirname(__file__), log_path)

    log_file = os.path.join(log_path, log_file_name)

    if os.path.isdir(log_path):
        if os.access(log_path, os.W_OK):
            return log_file
    else:
        try:
            os.makedirs(log_path)
            return log_file
        except Exception:
            pass


# return accessable log path or None
def get_accessible_log_path(reservation_id="Autoload", handler="default"):
    """Generate log path for the logger and verify that it's accessible.

     Using LOG_PATH/reservation_id/handler-%timestamp%.log

    :param reservation_id: part of log path
    :param handler: handler name for logger
    :return: generated log path
    """
    config = get_settings()
    time_format = config["TIME_FORMAT"] or DEFAULT_TIME_FORMAT
    log_file_name = "{0}--{1}.log".format(handler, datetime.now().strftime(time_format))

    log_path = _get_log_path_config(config)

    if log_path:
        env_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."
        )
        shell_name = os.path.basename(os.path.abspath(env_folder))
        log_path = os.path.join(log_path, reservation_id, shell_name)
        path = _prepare_log_path(log_path=log_path, log_file_name=log_file_name)
        if path:
            return path

    default_log_path = config.get("DEFAULT_LOG_PATH")

    if default_log_path:
        default_log_path = os.path.join(default_log_path, reservation_id)
        return _prepare_log_path(log_path=default_log_path, log_file_name=log_file_name)


def log_execution_info(logger_hdlr, exec_info):
    """Log provided execution information into provided logger on 'INFO' level."""
    if not hasattr(logger_hdlr, "info_logged"):
        logger_hdlr.info_logged = True
        logger_hdlr.info("--------------- Execution Info: ---------------------------")
        for key, val in exec_info.items():
            logger_hdlr.info("{0}: {1}".format(key.ljust(20), val))
        logger_hdlr.info(
            "-----------------------------------------------------------\n"
        )


def get_qs_logger(log_group="Ungrouped", log_category="QS", log_file_prefix="QS"):
    """Create cloudshell specific singleton logger.

    :param log_group: This folder will be grouped under this name.
    The default implementation of the group is a folder under the logs directory.
    According to the CloudShell logging standard pass the reservation id as this value
    when applicable, otherwise use the operation name (e.g 'Autoload').
    :type log_group: str

    :param log_category: All messages to this logger will be prefixed by the
    category name. The category name should be the name of the shell/driver
    :type log_category: str

    :param log_file_prefix: The log file generated by this logger will have this
    specified prefix. According to the logging standard the prefix should be the
    name of the resource the command is executing on. For environment commands
    use the command name.
    :type log_file_prefix: str

    :return: the logger object
    :rtype: logging.Logger
    """
    _LOGGER_LOCK.acquire()
    try:
        if log_group in _LOGGER_CONTAINER:
            logger = _LOGGER_CONTAINER[log_group]
        else:
            logger = _create_logger(log_group, log_category, log_file_prefix)
            _LOGGER_CONTAINER[log_group] = logger
    finally:
        _LOGGER_LOCK.release()

    return logger


def _create_logger(log_group, log_category, log_file_prefix):
    """Create logging handler.

    :param log_group: This folder will be grouped under this name.
    The default implementation of the group is a folder under the logs directory.
    According to the CloudShell logging standard pass the reservation id as this value
    when applicable, otherwise use the operation name (e.g 'Autoload').
    :type log_group: str

    :param log_category: All messages to this logger will be prefixed by the
    category name. The category name should be the name of the shell/driver
    :type log_category: str

    :param log_file_prefix: The log file generated by this logger will have this
    specified prefix. According to the logging standard the prefix should be the name
    of the resource the command is executing on. For environment commands
    use the command name.
    :type log_file_prefix: str

    :return: the logger object
    :rtype: logging.Logger
    """
    log_file_prefix = re.sub(" ", "_", log_file_prefix)
    log_category = "%s.%s" % (log_category, log_file_prefix)

    config = get_settings()

    if "LOG_LEVEL" in os.environ:
        log_level = os.environ["LOG_LEVEL"]
    elif config["LOG_LEVEL"]:
        log_level = config["LOG_LEVEL"]
    else:
        log_level = DEFAULT_LEVEL

    logger = logging.Logger(log_category, log_level)
    formatter = MultiLineFormatter(config["FORMAT"])
    log_path = get_accessible_log_path(log_group, log_file_prefix)

    if log_path:
        hdlr = MultiProcessingLog(log_path, mode="a")
    else:
        hdlr = StreamHandler(sys.stdout)

    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)

    return logger


def qs_time_this(func):
    """Decorator that reports the execution time."""  # noqa: D202

    @wraps(func)
    def wrapper(*args, **kwargs):
        _logger = get_qs_logger()
        start = time.time()
        _logger.info("%s started" % func.__name__)
        result = func(*args, **kwargs)
        end = time.time()
        _logger.info("%s ended taking %s" % (func.__name__, str(end - start)))
        return result

    return wrapper


def get_log_path(logger=logging.getLogger()):
    for hdlr in logger.handlers:
        if isinstance(hdlr, logging.FileHandler):
            return hdlr.baseFilename
    return None


def normalize_buffer(input_buffer):
    """Clear color from input_buffer and special characters.

    :param str input_buffer: input buffer string from device
    :return: str
    """
    # \033[1;32;40m
    # \033[ - Escape code
    # 1     - style
    # 32    - text color
    # 40    - Background colour
    color_pattern = re.compile(
        r"\[(\d+;){0,2}?\d+m|\b|" + chr(27)
    )  # 27 - ESC character

    result_buffer = ""

    if not isinstance(input_buffer, str):
        input_buffer = str(input_buffer)

    match_iter = color_pattern.finditer(input_buffer)

    current_index = 0
    for match_color in match_iter:
        match_range = match_color.span()
        result_buffer += input_buffer[current_index : match_range[0]]
        current_index = match_range[1]

    result_buffer += input_buffer[current_index:]

    result_buffer = result_buffer.replace("\r\n", "\n")

    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]", "", result_buffer)


class MultiLineFormatter(logging.Formatter):
    """Log Formatter, Append log header to each line."""

    MAX_SPLIT = 1

    def format(self, record):  # noqa: A003
        """Formatting for one or multi-line message.

        :param record:
        :return:
        """
        s = ""

        if record.msg == "":
            return s

        try:
            record.msg = normalize_buffer(record.msg)
            s = logging.Formatter.format(self, record)
            header, footer = s.rsplit(record.message, self.MAX_SPLIT)
            s = s.replace("\n", "\n" + header)
        except Exception as e:
            print(traceback.format_exc())  # noqa: T001
            print("logger.format: Unexpected error: " + str(e))  # noqa: T001
            print("record = {}<<<".format(traceback.format_exc()))  # noqa: T001
        return s


class Loggable(object):
    """Interface for Instances which uses Logging."""

    LOG_LEVEL = LOG_LEVELS["WARN"]  # Default Level that will be reported
    LOG_INFO = LOG_LEVELS["INFO"]
    LOG_WARN = LOG_LEVELS["WARN"]
    LOG_ERROR = LOG_LEVELS["ERROR"]
    LOG_CRITICAL = LOG_LEVELS["CRITICAL"]
    LOG_FATAL = LOG_LEVELS["FATAL"]
    LOG_DEBUG = LOG_LEVELS["DEBUG"]

    def setup_logger(self):
        """Setup local logger instance."""
        self.logger = get_qs_logger(self.__class__.__name__)
        self.logger.setLevel(self.LOG_LEVEL)
        # Logging methods aliases
        self.logDebug = self.logger.debug
        self.logInfo = self.logger.info
        self.logWarn = self.logger.warn
        self.logError = self.logger.error
