from django.http import HttpResponse, HttpRequest
from dss.Serializer import serializer

from django.conf import settings
import jwt  #需要安装pip install pyjwt
import datetime

import json
import logging
logger = logging.getLogger('django')

def safe_get_key(obj, key, placeholder=None):    
    try:
        val = obj.get(key)
        if val is None:
            return placeholder
        else:
            return val
    except:
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




