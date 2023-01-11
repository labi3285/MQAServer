from django.forms.models import model_to_dict
from django.core.paginator import Paginator

from django.conf import settings
import datetime
import traceback

from aws_mqaserver.utils import value
from aws_mqaserver.utils import validator
from aws_mqaserver.utils import response
from aws_mqaserver.utils import token
from aws_mqaserver.utils import ids

from aws_mqaserver.models import User

import json

import logging
logger = logging.getLogger('django')

# Login
def login(request):
    params = json.loads(request.body.decode())
    account = validator.validate_not_empty(params, 'account')
    passoword = validator.validate_not_empty(params, 'password')

    # admin
    if account == 'admin':
        if passoword != settings.ADMIN_PASSWORD:
            return response.ResponseError('Password Incorrect')
        id = -1
        lob = ''
        team = 'mqa'
        role = 'super_admin'
        _token = token.generate_token(id, team, account, lob, role)
        return response.ResponseData({
            'user': {
                'id': id,
                'team': team,
                'account': 'admin',
                'lob': ids.get_ids(lob),
                'role': role
            },
            'token': _token
        })
    
    # normal user
    try:
        user = User.objects.get(account=account)
        if user.status == 0:
            return response.ResponseError('User Disabled')
        if user.password != passoword:
            return response.ResponseError('Password Incorrect')
        _token = token.generate_token(user.id, user.team, user.account, user.lob, user.role)
        dict = model_to_dict(user)
        dict['password'] = None
        dict['lob'] = ids.get_ids(dict.get('lob'))
        return response.ResponseData({
            'user': dict,
            'token': _token
        })
    except User.DoesNotExist:
        return response.ResponseError('User Not Exist')
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')


def refresh_user(request):
    operator = validator.checkout_token_user(request)
    user = User.objects.get(id=operator.id)
    _token = token.generate_token(user.id, user.team, user.account, user.lob, user.role)
    dict = model_to_dict(user)
    dict['password'] = None
    dict['lob'] = ids.get_ids(dict.get('lob'))
    return response.ResponseData({
        'user': dict,
        'token': _token
    })




# Add Users
def add_user(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    team = validator.get_team(params, operator)
    account = validator.validate_not_empty(params, 'account')
    role = validator.validate_not_empty(params, 'role')
    lob = None
    if role != 'super_admin' and role != 'admin':
        lob = validator.validate_not_empty(params, 'lob')
        lob = ids.format_ids(lob)
    if operator.role != 'super_admin' and operator.role != 'admin':
        # Only admin can add admin or lob_dri
        if role == 'super_admin' or role == 'admin' or role == 'lob_dri':
            return response.ResponseError('Operation Forbidden')
        # Only admin or lob_dri can add user
        if operator.role != 'lob_dri':
            return response.ResponseError('Operation Forbidden')
        # Lob Manager can only add user in the same lob
        if not ids.contains_id(lob, operator.lob):
            return response.ResponseError('Operation Forbidden')
    # can not use name as 'admin'
    if account == 'admin':
        return response.ResponseError('Can Not Use This Name')
    # check duplicate name
    try:
        user = User.objects.get(account=account)
        return response.ResponseError('Account Duplicate')
    except User.DoesNotExist:
        pass
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')
    # add user
    try:
        user = User(account=account, team=team, role=role, lob=lob, password=settings.USER_DEFAULT_PASSWORD, createTime=datetime.datetime.now())
        user.save()
        return response.ResponseData('Add Success')
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')


# Change User Role
def change_user_role(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    id = validator.validate_not_empty(params, 'id')
    role = validator.validate_not_empty(params, 'role')
    lob = None
    if role != 'admin':
        lob = validator.validate_not_empty(params, 'lob')
        lob = ids.format_ids(lob)
    if operator.role != 'super_admin' and operator.role != 'admin':
        # Only admin can add admin or lob_dri
        if role == 'super_admin' or role == 'admin' or role == 'lob_dri':
            return response.ResponseError('Operation Forbidden')
        # Only admin or lob_dri can add user
        if operator.role != 'lob_dri':
            return response.ResponseError('Operation Forbidden')
        # Lob Manager can only add user in the same lob
        if not ids.contains_ids(lob, operator.lob):
            logger.info(operator.lob)
            logger.info(lob)

            return response.ResponseError('Operation Forbidden')
    try:
        user = User.objects.filter(id=id)
        user.update(role=role, lob=lob)
        return response.ResponseData('Role Changed')
    except User.DoesNotExist:
        return response.ResponseError('User Not Exist')
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')
    
# Get Users Page
def get_users_page(request):
    operator = validator.checkout_token_user(request)
    if operator.role != 'super_admin' and operator.role != 'admin' and operator.role != 'lob_dri':
        return response.ResponseError('Operation Forbidden')
    params = json.loads(request.body.decode())
    pageNum = validator.validate_not_empty(params, 'pageNum')
    pageSize = validator.validate_not_empty(params, 'pageSize')
    team = validator.get_team(params, operator)
    account = value.safe_get_in_key(params, 'account')
    role = value.safe_get_in_key(params, 'role')
    lob = value.safe_get_in_key(params, 'lob')
    try:
        list = User.objects.all().filter(team=team).order_by("createTime")
        if account != None:
            list = list.filter(account=account)
        if role != None:
            list = list.filter(role=role)
        if lob != None:
            list = list.filter(lob=lob)
        if list is None:
            return response.ResponseData({
                'total': 0,
                'list': []
            })
        paginator = Paginator(list, pageSize)
        page = paginator.get_page(pageNum)
        arr = []
        for user in page:
            dict = model_to_dict(user)
            dict['lob'] = ids.get_ids(dict.get('lob'))
            dict['password'] = None
            arr.append(dict)
        return response.ResponseData({
            'total': paginator.count,
            'list': arr
        })
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')
    
# Update User Status
def update_user_status(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    id = validator.validate_not_empty(params, 'id')    
    status = validator.validate_integer(params, 'status', min=0, max=1)    
    if operator.role != 'super_admin' and operator.role != 'admin' and operator.role != 'lob_dri':
        return response.ResponseError('Operation Forbidden')
    if operator.role == 'lob_dri':
        try:
            user = User.objects.get(id=id)
            # LOB Manager can not edit admin or LOB Manager
            if user.role == 'admin' or user.role == 'lob_dri':
                return response.ResponseError('Operation Forbidden')
            # LOB Manager can not edit users in other lobs
            if not ids.contains_ids(user.lob, operator.lob):
                return response.ResponseError('Operation Forbidden')
        except User.DoesNotExist:
            return response.ResponseError('User Not Exist')
        except Exception:
            traceback.print_exc()
            return response.ResponseError('System Error')
    try:
        user = User.objects.get(id=id)
        if user.id == operator.id:
            return response.ResponseError('Cannot Delete Self')
        user.status = status
        user.save()
        return response.ResponseData('Updated')
    except User.DoesNotExist:
        return response.ResponseError('User Not Exist')
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')
    
# Reset User Password
def reset_user_password(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    id = validator.validate_not_empty(params, 'id')    
    if operator.role != 'super_admin' and operator.role != 'admin' and operator.role != 'lob_dri':
        return response.ResponseError('Operation Forbidden')
    if operator.role == 'lob_dri':
        try:
            user = User.objects.get(id=id)
            # LOB Manager can not edit admin or LOB Manager
            if user.role == 'admin' or user.role == 'lob_dri':
                return response.ResponseError('Operation Forbidden')
            # LOB Manager can not edit users in other lobs
            if user.lob != operator.lob:
                return response.ResponseError('Operation Forbidden')
        except User.DoesNotExist:
            return response.ResponseError('User Not Exist')
        except Exception:
            traceback.print_exc()
            return response.ResponseError('System Error')
    try:
        user = User.objects.get(id=id)
        if user.id == operator.id:
            return response.ResponseError('Cannot Delete Self')
        user.password = settings.USER_DEFAULT_PASSWORD
        user.save()
        return response.ResponseData('Updated')
    except User.DoesNotExist:
        return response.ResponseError('User Not Exist')
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')
    
# Change User Password
def user_change_password(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    oldPassword = validator.validate_not_empty(params, 'oldPassword')
    newPassword = validator.validate_not_empty(params, 'newPassword')
    try:
        user = User.objects.get(id=operator.id)
        if user.password != oldPassword:
            return response.ResponseError('Password Incorrect')
        user.password = newPassword
        user.save()
        return response.ResponseData('Password Changed')
    except User.DoesNotExist:
        return response.ResponseError('User Not Exist')
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')
    
# Delete user
def delete_user(request):
    return response.ResponseError('Not Open')
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    id = validator.validate_not_empty(params, 'id')    
    if operator.role != 'super_admin' and operator.role != 'admin' and operator.role != 'lob_dri':
        return response.ResponseError('Operation Forbidden')
    if operator.role == 'lob_dri':
        try:
            user = User.objects.get(id=id)
            # LOB Manager can not delete admin or LOB Manager
            if user.role == 'admin' or user.role == 'lob_dri':
                return response.ResponseError('Operation Forbidden')
            # LOB Manager can not delete users in other lobs
            if not ids.contains_ids(user.lob, operator.lob):
                return response.ResponseError('Operation Forbidden')
        except User.DoesNotExist:
            return response.ResponseError('User Not Exist')
        except Exception:
            traceback.print_exc()
            return response.ResponseError('System Error')
    try:
        user = User.objects.get(id=id)
        if user.id == operator.id:
            return response.ResponseError('Cannot Delete Self')
        user.delete()
        return response.ResponseData('Deleted')
    except User.DoesNotExist:
        return response.ResponseError('User Not Exist')
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')
    
        



