
import datetime, time
import traceback

import json
import logging
logger = logging.getLogger('django')

def safe_get_in_key(obj, key, placeholder=None):
    try:
        val = obj.get(key)
        if val is None or val == '':
            return placeholder
        else:
            return val
    except:
        return placeholder

def safe_get_bool_in_key(params, key, placeholder=None):
    val = safe_get_in_key(params, key)
    if val == None or val == '':
        return placeholder
    if isinstance(val, bool):
        return val
    try:
        if isinstance(val, str):
            if val == '0' or val == 'False' or val == 'FALSE' or val == 'No' or val == 'NO' or val == 'N':
                return False
        i = bool(val)
        return i
    except Exception:
        return placeholder

def safe_get_float_in_key(params, key, min=None, max=None, placeholder=None):
    val = safe_get_in_key(params, key)
    if val == None or val == '':
        return placeholder
    try:
        i = float(val)
        if min != None:
            if i < min:
                return placeholder
        if max != None:
            if i > max:
                return placeholder
        return i
    except Exception:
        return placeholder

def safe_get_date_in_key(params, key, placeholder=None):
    d = safe_get_float_in_key(params, key)
    if d != None:
        try:
            date = datetime.datetime.fromtimestamp(d)
            return date
        except Exception:
            return placeholder
    return placeholder

def safe_get_in_keys(obj, keys, placeholder=None):
    for key in keys:
        val = safe_get_in_key(obj, key)
        if val != None:
            return val
    return placeholder

    
def empty(val):
    if val is None:
        return True
    elif val == '':
        return True
    elif val == '' or val == 'nan' or val == '/' or val == '-':
        return True
    elif val == 'NULL':
        return True
    elif str(val) == 'nan':
        return True
    return False




