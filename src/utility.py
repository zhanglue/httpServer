# -*- coding: utf-8 -*-

################################################################################
# Feature  : Common APIs.
# Author   : zhanglue
# Date     : 2019.01.24
################################################################################

import os

def path_join(*pathList):
    """
    Join path strings and return absolute path.
    """
    return get_abspath(os.path.join(*pathList))


def get_abspath(path):
    """
    Return absolute path.
    """
    return os.path.abspath(path)


def make_dir(dirPath, force=False):
    """
    Make directory.
    """
    if not dirPath:
        return

    if os.path.exists(dirPath):
        if not force:
            return
        remove_dir(dirPath)

    os.makedirs(dirPath)


def is_file_existing(fileToCheck):
    """
    Return if file is existing.
    """
    return isinstance(fileToCheck, str) and \
            len(fileToCheck) and \
            os.path.exists(fileToCheck) and \
            os.path.isfile(fileToCheck)


def is_dir_existing(dirToCheck):
    """
    Return if dir is existing.
    """
    return isinstance(dirToCheck, str) and \
            len(dirToCheck) and \
            os.path.exists(dirToCheck) and \
            os.path.isdir(dirToCheck)


def get_env_var(varName, isInt=False):
    """
    Get shell environment var.
    """
    result = None

    if varName not in os.environ:
        return result

    result = os.environ[varName]

    if isInt:
        result = int(result)

    return result


def is_port_idle(port):
    """
    Return if port is idle.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = get_host_ip()
    try:
        s.connect((ip, port))
        s.shutdown(2)
        return False
    except:
        return True

    return False


