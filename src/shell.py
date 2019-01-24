# -*- coding: utf-8 -*-

################################################################################
# Feature  : File APIs.
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


