import sys, os
from django.forms.models import model_to_dict
from django.db.models import Q
from django.db import transaction

from django.core.paginator import Paginator
import logging
from django.conf import settings
import datetime
import traceback

from aws_mqaserver.utils import value
from aws_mqaserver.utils import validator
from aws_mqaserver.utils import response
from aws_mqaserver.utils import token
from aws_mqaserver.utils import ids

from aws_mqaserver.team_SIP.models import SIPLineConfig

import json

logger = logging.getLogger('django')

def update_line_config(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    id = value.safe_get_in_key(params, 'id')
    lob = value.safe_get_in_key(params, 'lob')
    site = value.safe_get_in_key(params, 'site')
    productLine = value.safe_get_in_key(params, 'productLine')
    project = value.safe_get_in_key(params, 'project')
    part = value.safe_get_in_key(params, 'part')
    domain = validator.validate_not_empty(params, 'domain')
    data = value.safe_get_in_key(params, 'data', '')
    if part != None and project == None:
        return response.ResponseError('Params Error')
    if project != None and productLine == None:
        return response.ResponseError('Params Error')
    if productLine != None and site == None:
        return response.ResponseError('Params Error')
    if site != None and lob == None:
        return response.ResponseError('Params Error')
    if operator.role != 'super_admin' and operator.role != 'admin':
        # only lob_dri and admin can add line
        if operator.role != 'lob_dri':
            return response.ResponseError('Operation Forbidden')
        # lob_dri can only add lob sub line
        if site != None and not ids.contains_id(lob, operator.lob):
            return response.ResponseError('Operation Forbidden')
    if id == None:
        try:
            entry = SIPLineConfig.objects.get(lob=lob, site=site, productLine=productLine, project=project, part=part, domain=domain)
            entry.data = data
            entry.save()
            return response.ResponseData('Add Success')
        except SIPLineConfig.DoesNotExist:
            entry = SIPLineConfig(lob=lob, site=site, productLine=productLine, project=project, part=part,
                               domain=domain,
                               data=data)
            entry.save()
            return response.ResponseData('Add Success')
        except Exception:
            traceback.print_exc()
            return response.ResponseError('System Error')
    else:
        entry = SIPLineConfig.objects.get(id=id)
        entry.data = data
        entry.save()
        return response.ResponseData('Update Success')

def find_line_config_by_id(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    id = validator.validate_not_empty(params, 'id')
    entry = SIPLineConfig.objects.get(id=id)
    return response.ResponseData(model_to_dict(entry))

def find_line_config(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    domain = validator.validate_not_empty(params, 'domain')
    lob = validator.validate_not_empty(params, 'lob')
    site = value.safe_get_in_key(params, 'site')
    productLine = value.safe_get_in_key(params, 'productLine')
    project = value.safe_get_in_key(params, 'project')
    part = value.safe_get_in_key(params, 'part')
    if part != None and project == None:
        return response.ResponseError('Params Error')
    if project != None and productLine == None:
        return response.ResponseError('Params Error')
    if productLine != None and site == None:
        return response.ResponseError('Params Error')
    entry = None
    try:
        entry = SIPLineConfig.objects.get(lob=lob, site=site, productLine=productLine, project=project, part=part, domain=domain)
        return response.ResponseData(model_to_dict(entry))
    except SIPLineConfig.DoesNotExist:
        try:
            entry = SIPLineConfig.objects.get(lob=lob, site=site, productLine=productLine, project=project, part=None, domain=domain)
            return response.ResponseData(model_to_dict(entry))
        except SIPLineConfig.DoesNotExist:
            try:
                entry = SIPLineConfig.objects.get(lob=lob, site=site, productLine=productLine, project=None, part=None, domain=domain)
                return response.ResponseData(model_to_dict(entry))
            except SIPLineConfig.DoesNotExist:
                try:
                    entry = SIPLineConfig.objects.get(lob=lob, site=site, productLine=None, project=None, part=None, domain=domain)
                    return response.ResponseData(model_to_dict(entry))
                except SIPLineConfig.DoesNotExist:
                    try:
                        entry = SIPLineConfig.objects.get(lob=lob, site=None, productLine=None, project=None, part=None, domain=domain)
                        return response.ResponseData(model_to_dict(entry))
                    except SIPLineConfig.DoesNotExist:
                        try:
                            entry = SIPLineConfig.objects.get(lob=None, site=None, productLine=None, project=None, part=None, domain=domain)
                            return response.ResponseData(model_to_dict(entry))
                        except SIPLineConfig.DoesNotExist:
                            return response.ResponseData(None)
                        except Exception:
                            traceback.print_exc()
                            return response.ResponseError('System Error')
                    except Exception:
                        traceback.print_exc()
                        return response.ResponseError('System Error')
                except Exception:
                    traceback.print_exc()
                    return response.ResponseError('System Error')
            except Exception:
                traceback.print_exc()
                return response.ResponseError('System Error')
        except Exception:
            traceback.print_exc()
            return response.ResponseError('System Error')
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')

# Delete MIL Item
def delete_line_config_item(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    id = validator.validate_not_empty(params, 'id')
    entry = None
    try:
        entry = SIPLineConfig.objects.get(id=id)
    except SIPLineConfig.DoesNotExist:
        return response.ResponseError('Line Config Not Exist')
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')
    if operator.role != 'super_admin' and operator.role != 'admin':
        if operator.role != 'lob_dri':
            return response.ResponseError('Operation Forbidden')
        if not ids.contains_id(entry.lob, operator.lob):
            return response.ResponseError('Operation Forbidden')
    # delete
    try:
        entry.delete()
        return response.ResponseData('Deleted')
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')

def get_line_configs_page(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    pageNum = validator.validate_not_empty(params, 'pageNum')
    pageSize = validator.validate_not_empty(params, 'pageSize')
    lob = value.safe_get_in_key(params, 'lob')
    site = value.safe_get_in_key(params, 'site')
    productLine = value.safe_get_in_key(params, 'productLine')
    project = value.safe_get_in_key(params, 'project')
    part = value.safe_get_in_key(params, 'part')
    domain = value.safe_get_in_key(params, 'domain')
    if operator.role != 'super_admin' and operator.role != 'admin' and not ids.contains_id(lob, operator.lob):
        return response.ResponseError('Operation Forbidden')
    if part != None:
        if project == None:
            return response.ResponseError('Params Error')
    if project != None:
        if productLine == None:
            return response.ResponseError('Params Error')
    if productLine != None:
        if site == None or lob == None:
            return response.ResponseError('Params Error')
    if site != None:
        if lob == None:
            return response.ResponseError('Params Error')
    try:
        list = SIPLineConfig.objects.all()
        if lob != None:
            list = list.filter(lob=lob)
        if site != None:
            list = list.filter(site=site)
        if productLine != None:
            list = list.filter(productLine=productLine)
        if project != None:
            list = list.filter(project=project)
        if part != None:
            list = list.filter(part=part)
        if domain != None:
            list = list.filter(domain=domain)
        if list is None:
            return response.ResponseData({
                'total': 0,
                'list': []
            })
        paginator = Paginator(list, pageSize)
        page = paginator.get_page(pageNum)
        arr = []
        for e in page:
            arr.append(model_to_dict(e))
        return response.ResponseData({
            'total': paginator.count,
            'list': arr
        })
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')



