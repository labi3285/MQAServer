
from django.forms.models import model_to_dict
from django.db.models import Q
from django.db import transaction

from django.core.paginator import Paginator
import logging
from django.conf import settings
import datetime, time
import traceback

from aws_mqaserver.utils import value
from aws_mqaserver.utils import validator
from aws_mqaserver.utils import response
from aws_mqaserver.utils import token
from aws_mqaserver.utils import base64

from aws_mqaserver.models import MILItem

import json

logger = logging.getLogger('django')

# Get MIL Items Page
def get_mil_items_page(request):
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
    if operatorRole != 'admin':
        if operatorLob != lob:
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
        list = MILItem.objects.all()
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
            arr.append(model_to_dict(e))
        return response.ResponseData({
            'total': paginator.count,
            'list': arr
        })
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')
    
    
# Delete MIL Item
def delete_mil_item(request):
    tokenInfo = validator.check_token_info(request)
    operatorLob = tokenInfo.get('lob')
    operatorRole = tokenInfo.get('role')
    params = json.loads(request.body.decode())
    id = validator.validate_not_empty(params, 'id')
    entry = None
    try:
        entry = MILItem.objects.get(id=id)
    except MILItem.DoesNotExist:
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


def _batch_add_mil_items(auditItemId, lob, site, productLine, project, part, type, auditorId, auditor, dicArr):
    batch = []
    for e in dicArr:
        sn = validator.validate_integer(e, 'sn')
        type = value.safe_get_key(e, 'processType', type)
        createTime = validator.validate_date(e, 'createTime')
        year = createTime.year
        month = createTime.month
        week = int(createTime.strftime("%W")) + 1
        day = createTime.day
        quarter = None
        if month < 4:
            quarter = 1
        elif month < 7:
            quarter = 2
        elif month < 10:
            quarter = 3
        else:
            quarter = 4
        findings = validator.validate_not_empty(e, 'findings')
        keywords = value.safe_get_key(e, 'keywords')
        status = value.safe_get_key(e, 'status')
        severity = value.safe_get_key(e, 'severity')
        line = value.safe_get_key(e, 'line')
        station = value.safe_get_key(e, 'station')
        issueCategory = value.safe_get_key(e, 'issueCategory')
        subCategory = value.safe_get_key(e, 'subCategory')
        issueBrief = value.safe_get_key(e, 'issueBrief')
        containmentAction = value.safe_get_key(e, 'containmentAction')
        correctiveAction = value.safe_get_key(e, 'correctiveAction')
        department = value.safe_get_key(e, 'department')
        vendorDRI = value.safe_get_key(e, 'vendorDRI')
        item = MILItem(
            auditItemId=auditItemId,
            lob=lob,
            site=site,
            productLine=productLine,
            project=project,
            part=part,
            sn=sn,
            type=type,
            year=year,
            month=month,
            day=day,
            quarter=quarter,
            week=week,
            findings=findings,
            keywords=keywords,
            status=status,
            severity=severity,
            line=line,
            station=station,
            issueCategory=issueCategory,
            subCategory=subCategory,
            issueBrief=issueBrief,
            containmentAction=containmentAction,
            correctiveAction=correctiveAction,
            department=department,
            vendorDRI=vendorDRI,
            createTime=createTime,
            auditorId=auditorId,
            auditor=auditor,
        )
        batch.append(item)
    if len(batch) > 0:
        MILItem.objects.bulk_create(batch, batch_size=len(batch))

