from django.conf import settings
import jwt  #需要安装pip install pyjwt
import datetime
import traceback

from aws_mqaserver.defines import ValidateException 

import logging
logger = logging.getLogger('django')

def generate_token(id, team, name, lob, role):
    try:
        payload = {
            'id': id,
            'team': team,
            'name': name,
            'lob': lob,
            'role': role,
            'exp': datetime.datetime.now() + datetime.timedelta(seconds=60 * 60 * 24 * 30)
        }
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')
        t = '%s'%token
        if t.startswith('b\''):
            t = t[2:]
        if t.endswith('\''):
            t = t[0:-1]
        return t
    except Exception as e:
        traceback.print_exc()
        raise ValidateException('Generate Token Failed', e)

def checkout_token_info(token_str):
    t = token_str
    if t.startswith('b\''):
        t = t[2:]
    if t.endswith('\''):
        t = t[0:-1]
    try:
        info = jwt.decode(t, key=settings.SECRET_KEY, algorithm='HS256', algorithms=['HS256'])
        return info
    except jwt.ExpiredSignatureError:
        raise ValidateException('User Token Validate Failed')
    except jwt.exceptions.ExpiredSignatureError:
        raise ValidateException('User Token Expired, Please Re-Login')
    except Exception as e:
        traceback.print_exc()
        raise ValidateException('Checkout Token Failed', e)


class TokenUser:
    id = None
    team = None
    name = None
    lob = None
    role = None

def checkout_token_user(token_str):
    dic = checkout_token_info(token_str)
    user = TokenUser()
    user.id = dic.get('id')
    user.team = dic.get('team')
    user.name = dic.get('name')
    user.lob = dic.get('lob')
    user.role = dic.get('role')
    return user
