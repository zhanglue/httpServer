# -*- coding: utf-8 -*-

################################################################################
# Feature  : Load/save json from/to file.
# Author   : zhanglue
# Date     : 2019.01.25
################################################################################

import sys
import codecs
import json

from utility import is_file_existing
from log import TheLogger

def _byteify(data, ignore_dicts = False):
    """
    Hook function for json load/loads.
    """
    if sys.version < "3" and isinstance(data, unicode):
        return data.encode("utf-8")
    elif sys.version > "3" and isinstance(data, bytes):
        return data.encode("utf-8")
    elif isinstance(data, list):
        return [_byteify(item, ignore_dicts) for item in data]
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts): _byteify(value, ignore_dicts)
            for key, value in data.items()
        }
    return data


def json_load_byteified(file_handle):
    """
    Package json load with hook.
    """
    try:
        result = _byteify(json.load(file_handle, object_hook = _byteify),
                ignore_dicts = True)
    except Exception as e:
        TheLogger.error("Json load failed: %s" % str(e))
        return None

    return result

def json_loads_byteified(json_text):
    """
    Package json loads with hook.
    """
    try:
        result = _byteify(json.loads(json_text, object_hook = _byteify),
                ignore_dicts = True)
    except Exception as e:
        TheLogger.error("Json load failed: %s" % str(e))
        return None

    return result


def json_file_to_pyData(jsonFile):
    """
    Convert json file to python data.
    """
    if not is_file_existing(jsonFile):
        TheLogger.error("Json file is not found: %s" % jsonFile)
        return None

    with codecs.open(jsonFile, encoding="utf-8") as f:
        try:
            return json_load_byteified(f)
        except Exception as e:
            return None


def json_dumps(inputData):
    """
    Dump json data.
    """
    if isinstance(inputData, str):
        return inputData

    return json.dumps(inputData, indent = 4, 
            sort_keys = True, ensure_ascii = False)


def json_loads(inputStr):
    """
    Load str to dict.
    """
    #return json_loads_byteified(inputStr)
    return json.loads(inputStr)


def pyData_to_json_file(inputData, outputFile):
    """
    Convert python data to json file.
    """
    with open(outputFile, "w") as f:
        f.write(json_dumps(inputData)+"\n")


