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
from aws_mqaserver.utils import base64
from aws_mqaserver.utils import ids

from aws_mqaserver.team_MDE.models import MDELine
from aws_mqaserver.team_MDE.models import MDECheckList
from aws_mqaserver.team_MDE.apis import check_list_item

import json

logger = logging.getLogger('django')

# Admin Upload CheckList
@transaction.atomic
def upload_check_list(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    lob = validator.validate_not_empty(params, 'lob')
    site = validator.validate_not_empty(params, 'site')
    productLine = validator.validate_not_empty(params, 'productLine')
    project = validator.validate_not_empty(params, 'project')
    part = value.safe_get_in_key(params, 'part', '')
    rawJsonBase64 = validator.validate_not_empty(params, 'rawJson')
    rawJson = base64.base64ToString(rawJsonBase64)
    if operator.role != 'super_admin' and operator.role != 'admin':
        if not ids.contains_id(lob, operator.lob):
            return response.ResponseError('Operation Forbidden')
    # add
    try:
        entry = MDECheckList(lob=lob, site=site, productLine=productLine, project=project, part=part,
                             createTime=datetime.datetime.now(), updaterId=operator.id, updater=operator.name)
        entry.save()
        check_list_item._batch_add_check_list_items(entry.id, json.loads(rawJson))
        line = MDELine.objects.get(lob=lob, site=site, productLine=productLine, project=project, part=None)
        line.checkListId = entry.id
        line.save()
        return response.ResponseData('Uploaded')
    except Exception as e:
        traceback.print_exc()
        raise e

# Get CheckLists Page
def get_check_lists_page(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    pageNum = validator.validate_not_empty(params, 'pageNum')
    pageSize = validator.validate_not_empty(params, 'pageSize')
    lob = value.safe_get_in_key(params, 'lob')
    site = value.safe_get_in_key(params, 'site')
    productLine = value.safe_get_in_key(params, 'productLine')
    project = value.safe_get_in_key(params, 'project')
    part = value.safe_get_in_key(params, 'part')
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
        list = MDECheckList.objects.all()
        if lob != None:
            list = list.filter(lob=lob)
        if site != None:
            list = list.filter(site=site)
        if productLine != None:
            list = list.filter(productLine=productLine)
        if project != None:
            list = list.filter(project=project)
        list = list.order_by('-createTime')
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

    
# Delete Check List
def delete_check_list(request):
    operator = validator.checkout_token_user(request)
    if operator.role != 'admin' and operator.role != 'lob_dri':
        return response.ResponseError('Operation Forbidden')
    params = json.loads(request.body.decode())
    id = validator.validate_not_empty(params, 'id')
    entry = None
    try:
        entry = MDECheckList.objects.get(id=id)
    except MDECheckList.DoesNotExist:
        return response.ResponseError('Check List Not Exist')
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')
    if operator.role != 'super_admin' and operator.role != 'admin':
        # lob_dri can only delete check list in his lob
        if not ids.contains_id(lob, operator.lob):
            return response.ResponseError('Operation Forbidden')
    # delete
    try:
        entry.delete()
        return response.ResponseData('Deleted')        
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')