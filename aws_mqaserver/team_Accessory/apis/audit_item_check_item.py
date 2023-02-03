import sys, os
from django.forms.models import model_to_dict
from django.db.models import Q
from django.db import transaction

from django.core.paginator import Paginator
import logging
from django.conf import settings
import datetime, time
import traceback

import pandas
from django.core.files import temp as tempfile
from aws_mqaserver.apis import box

from aws_mqaserver.utils import value
from aws_mqaserver.utils import validator
from aws_mqaserver.utils import response
from aws_mqaserver.utils import token
from aws_mqaserver.utils import base64
from aws_mqaserver.utils import ids

from aws_mqaserver.team_Accessory.models import AccessoryCheckType
from aws_mqaserver.team_Accessory.models import AccessoryAuditItemCheckItemGlue
from aws_mqaserver.team_Accessory.models import AccessoryAuditItemCheckItemGluePoint
from aws_mqaserver.team_Accessory.models import AccessoryAuditItemCheckItemDestructive
from aws_mqaserver.team_Accessory.models import AccessoryAuditItemCheckItemDestructivePoint

import json

logger = logging.getLogger('django')

# Get Audit Check Items Page
def get_audit_item_check_items_page_glue(request):
    return _get_audit_item_check_items_page(request, 'Glue')
def get_audit_item_check_items_page_destructive(request):
    return _get_audit_item_check_items_page(request, 'Destructive')
def _get_audit_item_check_items_page(request, type):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    pageNum = validator.validate_not_empty(params, 'pageNum')
    pageSize = validator.validate_not_empty(params, 'pageSize')
    auditItemId = validator.validate_not_empty(params, 'auditItemId')
    try:
        list = None
        if type == AccessoryCheckType.Glue:
            list = AccessoryAuditItemCheckItemGlue.objects.all().filter(auditItemId=auditItemId).order_by("sn")
        elif type == AccessoryCheckType.Destructive:
            list = AccessoryAuditItemCheckItemDestructive.objects.all().filter(auditItemId=auditItemId).order_by("sn")
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

def _batch_add_check_items(auditItemId, lob, site, productLine, project, part, type, auditorId, auditor, uploadTime, dicArr):
    batch = []
    if type == AccessoryCheckType.Glue:
        for e in dicArr:
            check_item = e['checkItem']
            checkListId = value.safe_get_in_key(check_item, 'checkListId')
            checkItem_sn = value.safe_get_in_key(check_item, 'sn')
            checkItem_theClass = value.safe_get_in_key(check_item, 'theClass', '')
            checkItem_lineShift = value.safe_get_in_key(check_item, 'lineShift', '')
            checkItem_site = value.safe_get_in_key(check_item, 'site', '')
            checkItem_projects = value.safe_get_in_key(check_item, 'projects', '')
            checkItem_item = value.safe_get_in_key(check_item, 'item', '')
            checkItem_unit = value.safe_get_in_key(check_item, 'unit', '')
            checkItem_LSL = value.safe_get_in_key(check_item, 'LSL', '')
            checkItem_USL = value.safe_get_in_key(check_item, 'USL', '')
            passCount = value.safe_get_in_key(e, 'passCount', 0)
            failCount = value.safe_get_in_key(e, 'failCount', 0)
            totalCount = value.safe_get_in_key(e, 'totalCount', 0)
            isDone = value.safe_get_bool_in_key(e, 'isDone', False)
            status = value.safe_get_in_key(e, 'status')
            createTime = value.safe_get_date_in_key(e, 'createTime')
            item = AccessoryAuditItemCheckItemGlue(
                auditItemId=auditItemId,
                lob=lob,
                site=site,
                productLine=productLine,
                project=project,
                part=part,
                checkListId=checkListId,
                checkItem_sn=checkItem_sn,
                checkItem_theClass=checkItem_theClass,
                checkItem_lineShift=checkItem_lineShift,
                checkItem_site=checkItem_site,
                checkItem_projects=checkItem_projects,
                checkItem_item=checkItem_item,
                checkItem_unit=checkItem_unit,
                checkItem_LSL=checkItem_LSL,
                checkItem_USL=checkItem_USL,
                passCount=passCount,
                failCount=failCount,
                totalCount=totalCount,
                isDone=isDone,
                status=status,
                createTime=createTime,
                uploadTime=uploadTime,
                auditorId=auditorId,
                auditor=auditor,
            )
            batch.append(item)
        if len(batch) > 0:
            AccessoryAuditItemCheckItemGlue.objects.bulk_create(batch, batch_size=len(batch))

    elif type == AccessoryCheckType.Destructive:
        for e in dicArr:
            check_item = e['checkItem']
            checkListId = value.safe_get_in_key(check_item, 'checkListId')
            checkItem_sn = value.safe_get_in_key(check_item, 'sn')
            checkItem_theClass = value.safe_get_in_key(check_item, 'theClass', '')
            checkItem_lineShift = value.safe_get_in_key(check_item, 'lineShift', '')
            checkItem_site = value.safe_get_in_key(check_item, 'site', '')
            checkItem_projects = value.safe_get_in_key(check_item, 'projects', '')
            checkItem_item = value.safe_get_in_key(check_item, 'item', '')
            checkItem_unit = value.safe_get_in_key(check_item, 'unit', '')
            checkItem_LSL = value.safe_get_in_key(check_item, 'LSL', '')
            checkItem_USL = value.safe_get_in_key(check_item, 'USL', '')
            passCount = value.safe_get_in_key(e, 'passCount', 0)
            failCount = value.safe_get_in_key(e, 'failCount', 0)
            totalCount = value.safe_get_in_key(e, 'totalCount', 0)
            isDone = value.safe_get_bool_in_key(e, 'isDone', False)
            status = value.safe_get_in_key(e, 'status')
            createTime = value.safe_get_date_in_key(e, 'createTime')
            item = AccessoryAuditItemCheckItemDestructive(
                auditItemId=auditItemId,
                lob=lob,
                site=site,
                productLine=productLine,
                project=project,
                part=part,
                checkListId=checkListId,
                checkItem_sn=checkItem_sn,
                checkItem_theClass=checkItem_theClass,
                checkItem_lineShift=checkItem_lineShift,
                checkItem_site=checkItem_site,
                checkItem_projects=checkItem_projects,
                checkItem_item=checkItem_item,
                checkItem_unit=checkItem_unit,
                checkItem_LSL=checkItem_LSL,
                checkItem_USL=checkItem_USL,
                passCount=passCount,
                failCount=failCount,
                totalCount=totalCount,
                isDone=isDone,
                status=status,
                createTime=createTime,
                uploadTime=uploadTime,
                auditorId=auditorId,
                auditor=auditor,
            )
            batch.append(item)
        if len(batch) > 0:
            AccessoryAuditItemCheckItemDestructive.objects.bulk_create(batch, batch_size=len(batch))

def _batch_add_check_items_points(auditItemId, lob, site, productLine, project, part, type, auditorId, auditor, uploadTime, dicArr):
    batch = []
    if type == AccessoryCheckType.Glue:
        for e in dicArr:
            check_item = e['checkItem']
            checkListId = value.safe_get_in_key(check_item, 'checkListId')
            checkItem_sn = value.safe_get_in_key(check_item, 'sn')
            checkItem_theClass = value.safe_get_in_key(check_item, 'theClass', '')
            checkItem_lineShift = value.safe_get_in_key(check_item, 'lineShift', '')
            checkItem_site = value.safe_get_in_key(check_item, 'site', '')
            checkItem_projects = value.safe_get_in_key(check_item, 'projects', '')
            checkItem_item = value.safe_get_in_key(check_item, 'item', '')
            checkItem_unit = value.safe_get_in_key(check_item, 'unit', '')
            checkItem_LSL = value.safe_get_in_key(check_item, 'LSL', '')
            checkItem_USL = value.safe_get_in_key(check_item, 'USL', '')
            before = value.safe_get_in_key(e, 'before', 0)
            after = value.safe_get_in_key(e, 'after', 0)
            result = value.safe_get_in_key(e, 'result', 0)
            outOfSpec = value.safe_get_bool_in_key(e, 'outOfSpec', False)
            createTime = value.safe_get_date_in_key(e, 'createTime')
            item = AccessoryAuditItemCheckItemGluePoint(
                auditItemId=auditItemId,
                lob=lob,
                site=site,
                productLine=productLine,
                project=project,
                part=part,
                checkListId=checkListId,
                checkItem_sn=checkItem_sn,
                checkItem_theClass=checkItem_theClass,
                checkItem_lineShift=checkItem_lineShift,
                checkItem_site=checkItem_site,
                checkItem_projects=checkItem_projects,
                checkItem_item=checkItem_item,
                checkItem_unit=checkItem_unit,
                checkItem_LSL=checkItem_LSL,
                checkItem_USL=checkItem_USL,
                before=before,
                after=after,
                result=result,
                outOfSpec=outOfSpec,
                createTime=createTime,
                uploadTime=uploadTime,
                auditorId=auditorId,
                auditor=auditor,
            )
            batch.append(item)
        if len(batch) > 0:
            AccessoryAuditItemCheckItemGluePoint.objects.bulk_create(batch, batch_size=len(batch))

    elif type == AccessoryCheckType.Destructive:
        for e in dicArr:
            check_item = e['checkItem']
            checkListId = value.safe_get_in_key(check_item, 'checkListId')
            checkItem_sn = value.safe_get_in_key(check_item, 'sn')
            checkItem_theClass = value.safe_get_in_key(check_item, 'theClass', '')
            checkItem_lineShift = value.safe_get_in_key(check_item, 'lineShift', '')
            checkItem_site = value.safe_get_in_key(check_item, 'site', '')
            checkItem_projects = value.safe_get_in_key(check_item, 'projects', '')
            checkItem_item = value.safe_get_in_key(check_item, 'item', '')
            checkItem_unit = value.safe_get_in_key(check_item, 'unit', '')
            checkItem_LSL = value.safe_get_in_key(check_item, 'LSL', '')
            checkItem_USL = value.safe_get_in_key(check_item, 'USL', '')
            result = value.safe_get_in_key(e, 'result', 0)
            outOfSpec = value.safe_get_bool_in_key(e, 'outOfSpec', False)
            createTime = value.safe_get_date_in_key(e, 'createTime')
            item = AccessoryAuditItemCheckItemDestructivePoint(
                auditItemId=auditItemId,
                lob=lob,
                site=site,
                productLine=productLine,
                project=project,
                part=part,
                checkListId=checkListId,
                checkItem_sn=checkItem_sn,
                checkItem_theClass=checkItem_theClass,
                checkItem_lineShift=checkItem_lineShift,
                checkItem_site=checkItem_site,
                checkItem_projects=checkItem_projects,
                checkItem_item=checkItem_item,
                checkItem_unit=checkItem_unit,
                checkItem_LSL=checkItem_LSL,
                checkItem_USL=checkItem_USL,
                result=result,
                outOfSpec=outOfSpec,
                createTime=createTime,
                uploadTime=uploadTime,
                auditorId=auditorId,
                auditor=auditor,
            )
            batch.append(item)
        if len(batch) > 0:
            AccessoryAuditItemCheckItemDestructivePoint.objects.bulk_create(batch, batch_size=len(batch))