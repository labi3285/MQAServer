
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

from aws_mqaserver.models import CheckList
from aws_mqaserver.apis import check_list_item

import json

logger = logging.getLogger('django')

# Admin Upload CheckList
@transaction.atomic
def upload_check_list(request):
    tokenInfo = validator.check_token_info(request)
    operatorName = tokenInfo.get('name')
    operatorId = tokenInfo.get('id')
    operatorLob = tokenInfo.get('lob')
    operatorRole = tokenInfo.get('role')
    params = json.loads(request.body.decode())
    lob = validator.validate_not_empty(params, 'lob')
    site = validator.validate_not_empty(params, 'site')
    productLine = validator.validate_not_empty(params, 'productLine')
    project = validator.validate_not_empty(params, 'project')
    part = validator.validate_not_empty(params, 'part')
    type = validator.validate_integer(params, 'type')
    rawJsonBase64 = validator.validate_not_empty(params, 'rawJson')
    rawJson = base64.base64ToString(rawJsonBase64)
    if operatorRole != 'admin':
        if lob != operatorLob:
            return response.ResponseError('Operation Forbidden')
    # add
    try:
        entry = CheckList.objects.get(lob=lob, site=site, productLine=productLine, project=project, part=part, type=type)
        entry.rawJson = rawJson
        entry.updateTime = datetime.datetime.now()
        entry.updaterId = operatorId
        entry.updater = operatorName
        entry.save()
        check_list_item._batch_delete_check_list_items(entry.id, type)
        check_list_item._batch_add_check_list_items(entry.id, type, json.loads(rawJson))
        return response.ResponseData('Uploaded')
    except CheckList.DoesNotExist:
        entry = CheckList(lob=lob, site=site, productLine=productLine, project=project, part=part, type=type, rawJson=rawJson, createTime=datetime.datetime.now(), updaterId = operatorId, updater = operatorName)
        entry.save()
        check_list_item._batch_add_check_list_items(entry.id, type, json.loads(rawJson))
        return response.ResponseData('Uploaded')
    except Exception as e:
        traceback.print_exc()
        raise e

# Get CheckLists Page
def get_check_lists_page(request):
    tokenInfo = validator.check_token_info(request)
    operatorRole = tokenInfo.get('role')
    operatorLob = tokenInfo.get('lob')
    params = json.loads(request.body.decode())
    pageNum = validator.validate_not_empty(params, 'pageNum')
    pageSize = validator.validate_not_empty(params, 'pageSize')
    lob = value.safe_get_key(params, 'lob')
    site = value.safe_get_key(params, 'site')
    productLine = value.safe_get_key(params, 'productLine')
    project = value.safe_get_key(params, 'project')
    part = value.safe_get_key(params, 'part')
    if operatorRole != 'admin' and operatorLob != lob:
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
        list = CheckList.objects.defer('rawJson').all()
        if lob != None:
            list = list.filter(lob=lob)
        if site != None:
            list = list.filter(site=site)
        if productLine != None:
            list = list.filter(productLine=productLine)
        if project != None:
            list = list.filter(project=project)
        if list is None:
            return response.ResponseData({
                'total': 0,
                'list': []
            })
        paginator = Paginator(list, pageSize)
        page = paginator.get_page(pageNum)
        arr = []
        for e in page:
            arr.append({
                'id': e.id,
                'type': e.type,
                'lob': e.lob,
                'site': e.site,
                'productLine': e.productLine,
                'project': e.project,
                'part': e.part,
                'updateTime': e.updateTime,
                'createTime': e.createTime,
            })
        return response.ResponseData({
            'total': paginator.count,
            'list': arr
        })
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')

# Find One Check List
def find_check_list(request):
    tokenInfo = validator.check_token_info(request)
    params = json.loads(request.body.decode())
    lob = validator.validate_not_empty(params, 'lob')
    site = validator.validate_not_empty(params, 'site')
    productLine = validator.validate_not_empty(params, 'productLine')
    project = validator.validate_not_empty(params, 'project')
    part = validator.validate_not_empty(params, 'part')
    type = validator.validate_not_empty(params, 'type')
    try:
        e = CheckList.objects.defer('rawJson').get(lob=lob, site=site, productLine=productLine, project=project, part=part, type=type)
        m = {
            'id': e.id,
            'type': e.type,
            'lob': e.lob,
            'site': e.site,
            'productLine': e.productLine,
            'project': e.project,
            'part': e.part,
            'updateTime': e.updateTime,
            'createTime': e.createTime,
        }
        return response.ResponseData(m)
    except CheckList.DoesNotExist:
        return response.ResponseData(None)
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')

    
# Delete Check List
def delete_check_list(request):
    tokenInfo = validator.check_token_info(request)
    operatorLob = tokenInfo.get('lob')
    operatorRole = tokenInfo.get('role')
    if operatorRole != 'admin' and operatorRole != 'lob_manager':
        return response.ResponseError('Operation Forbidden')
    params = json.loads(request.body.decode())
    id = validator.validate_not_empty(params, 'id')
    entry = None
    try:
        entry = CheckList.objects.get(id=id)
    except CheckList.DoesNotExist:
        return response.ResponseError('Check List Not Exist')
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')
    if operatorRole != 'admin':
        # lob_manager can only delete check list in his lob
        if entry.lob != operatorLob:
            return response.ResponseError('Operation Forbidden')
    # delete
    try:
        entry.delete()
        return response.ResponseData('Deleted')        
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')