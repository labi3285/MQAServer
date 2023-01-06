from aws_mqaserver.utils import value
from aws_mqaserver.utils import token
from aws_mqaserver.defines import ValidateException 
import datetime, time

import logging
logger = logging.getLogger('django')

def check_token_info(request):
    _token = request.headers.get("Authorization")
    if _token == None:
        raise ValidateException('token empty')
    return token.checkout_token_info(_token)

def checkout_token_user(request):
    _token = request.headers.get("Authorization")
    if _token == None:
        raise ValidateException('token empty')
    return token.checkout_token_user(_token)

def validate_admin(request):
    token_info = check_token_info(request)
    if token_info.get('role') != 'admin':
        raise ValidateException('Operation Forbidden')
        
def validate_not_empty(params, key):
    if value.safe_get_in_key(params, key) == None:
        raise ValidateException(key + ' Empty')
    return params.get(key)

def get_team(params, operator):
    team = operator.team
    if operator.role == 'super_admin':
        return value.safe_get_in_key(params, 'team', 'mqa')
    else:
        return operator.team
def validate_not_empty_in_keys(params, keys):
    for key in keys:
        val = value.safe_get_in_key(params, key)
        if val != None:
            return val
    raise ValidateException(keys[0] + ' Empty')

def validate_integer(params, key, min=None, max=None):
    val = validate_not_empty(params, key)
    try:
        i = int(val)
        if min != None:
            if i < min:
                raise ValidateException(key + ' Invalid')
        if max != None:
            if i > max:
                raise ValidateException(key + ' Invalid')
        return i
    except Exception:
        raise ValidateException(key + ' Invalid')

def validate_float(params, key, min=None, max=None):
    val = validate_not_empty(params, key)
    try:
        i = float(val)
        if min != None:
            if i < min:
                raise ValidateException(key + ' Invalid')
        if max != None:
            if i > max:
                raise ValidateException(key + ' Invalid')
        return i
    except Exception:
        raise ValidateException(key + ' Invalid')

def validate_date(params, key):
    d = validate_float(params, key)
    try:
        date = datetime.datetime.fromtimestamp(d)
        return date
    except Exception:
        raise ValidateException(key + ' Invalid')
