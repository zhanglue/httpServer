# -*- coding: utf-8 -*-

################################################################################
##  Feature  : Log interface.
##  Author   : zhanglue
##  Date     : 2019.01.24
################################################################################

import os
import shutil
import logging
import logging.handlers

def init_logger(logPath=None, logFilePrefix=None, removeFormer=False, forbiddenStd=False):
    """
    Initialize logging module.
    """
    # Generate base logger.
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

    if not forbiddenStd:
        # Set stream logger.
        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(logging.INFO)

        debugLevelFlag = 0
        if "LOG_LEVEL_DEBUG" in os.environ:
            debugLevelFlag = os.environ["LOG_LEVEL_DEBUG"]

        if debugLevelFlag:
            streamHandler.setLevel(logging.DEBUG)
        else:
            streamHandler.setLevel(logging.INFO)
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)

    if not logPath:
        return logger

    # Set file logger:
    # 1. There are two log files: logFilePrefix.debug/logFilePrefix.we
    # 2. Log files devide to 100MB for each log file.
    # 3. It keeps last 10 log files.

    if not logFilePrefix:
        logFilePrefix = "main.log"
    try:
        if os.path.exists(logPath):
            if removeFormer:
                shutil.rmtree(logPath)
        else:
            os.makedirs(logPath)

        logFileName = "%s/%s.debug" % (logPath, logFilePrefix)
        fileHandler = logging.handlers.RotatingFileHandler(
                logFileName,
                maxBytes = 100 * 1024 * 1024,
                backupCount = 10)
        fileHandler.setLevel(logging.DEBUG)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
    except IOError as e:
        logger.error("Genrate log file in %s failed." % logPath)
        exit(2)

    try:
        logFileName = "%s/%s.we" % (logPath, logFilePrefix)
        fileHandler = logging.handlers.RotatingFileHandler(
                logFileName,
                maxBytes = 100 * 1024 * 1024,
                backupCount = 10)
        fileHandler.setLevel(logging.WARNING)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
    except IOError as e:
        logger.error("Genrate log file in %s failed." % logPath)
        exit(2)

    return logger


class TheLogger():
    """
    Static class.
    """
    _logger = None

    @classmethod
    def init(cls, logPath=None, logFilePrefix=None, removeFormer=False, forbiddenStd=False):
        """
        Initialization.
        """
        if not cls._logger:
            cls._logger = init_logger(logPath, logFilePrefix, removeFormer, forbiddenStd)

    @classmethod
    def debug(cls, *msgs):
        """
        Log debug.
        """
        if not cls._logger:
            TheLogger.init()
        cls._logger.debug("".join(msgs))

    @classmethod
    def info(cls, *msgs):
        """
        Log info.
        """
        if not cls._logger:
            TheLogger.init()
        cls._logger.info("".join(msgs))

    @classmethod
    def warning(cls, *msgs):
        """
        Log warning.
        """
        if not cls._logger:
            TheLogger.init()
        cls._logger.warning("".join(msgs))

    @classmethod
    def error(cls, *msgs):
        """
        Log error.
        """
        if not cls._logger:
            TheLogger.init()
        cls._logger.error("".join(msgs))

