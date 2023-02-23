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

from aws_mqaserver.team_MDE.models import MDEAuditItemCheckItem

import json

logger = logging.getLogger('django')

# Get Audit Check Items Page
def get_audit_item_check_items_page(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    pageNum = validator.validate_not_empty(params, 'pageNum')
    pageSize = validator.validate_not_empty(params, 'pageSize')
    auditItemId = validator.validate_not_empty(params, 'auditItemId')
    try:
        list = MDEAuditItemCheckItem.objects.all().filter(auditItemId=auditItemId).order_by("sn")
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

def _batch_add_check_items(auditItemId, lob, site, productLine, project, part, auditorId, auditor, uploadTime, dicArr):
    batch = []
    for e in dicArr:
        checkListId = value.safe_get_in_key(e, 'checkListId')
        checkItem_sn = value.safe_get_in_key(e, 'sn')
        checkItem_station = value.safe_get_in_key(e, 'station', '')
        checkItem_process = value.safe_get_in_key(e, 'process', '')
        checkItem_productLine = value.safe_get_in_key(e, 'productLine', '')
        checkItem_project = value.safe_get_in_key(e, 'project', '')
        checkItem_checkItem = value.safe_get_in_key(e, 'checkItem', '')
        checkItem_LSL = value.safe_get_in_key(e, 'LSL', 0)
        checkItem_USL = value.safe_get_in_key(e, 'USL', 0)
        _value = value.safe_get_in_key(e, 'value')
        if _value != None:
            _value = str(_value)
        status = value.safe_get_in_key(e, 'status')
        createTime = value.safe_get_date_in_key(e, 'createTime')
        item = MDEAuditItemCheckItem(
            auditItemId=auditItemId,
            lob=lob,
            site=site,
            productLine=productLine,
            project=project,
            part=part,
            checkListId=checkListId,
            checkItem_sn=checkItem_sn,
            checkItem_station=checkItem_station,
            checkItem_process=checkItem_process,
            checkItem_productLine=checkItem_productLine,
            checkItem_project=checkItem_project,
            checkItem_checkItem=checkItem_checkItem,
            checkItem_LSL=checkItem_LSL,
            checkItem_USL=checkItem_USL,
            value=_value,
            status=status,
            createTime=createTime,
            uploadTime=uploadTime,
            auditorId=auditorId,
            auditor=auditor,
        )
        batch.append(item)
    if len(batch) > 0:
        MDEAuditItemCheckItem.objects.bulk_create(batch, batch_size=len(batch))
