import sys, os
from django.forms.models import model_to_dict
from django.db.models import Q
from django.db import transaction
from django.core.paginator import Paginator

import pandas
from django.core.files import temp as tempfile
from aws_mqaserver.apis import box

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

from aws_mqaserver.team_MDE.models import MDEAuditItem

from aws_mqaserver.team_MDE.apis import audit_item_check_item

import json

logger = logging.getLogger('django')
logger.setLevel(logging.INFO)

@transaction.atomic
def upload_audit_item(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    logger.info(params)
    lob = validator.validate_not_empty(params, 'lob')
    site = validator.validate_not_empty(params, 'site')
    productLine = validator.validate_not_empty(params, 'productLine')
    project = validator.validate_not_empty(params, 'project')
    part = validator.validate_not_empty(params, 'part')
    beginTime = validator.validate_date(params, 'beginTime')
    endTime = validator.validate_date(params, 'endTime')
    crossDays = value.safe_get_in_key(params, 'crossDays')
    auditRemark = value.safe_get_in_key(params, 'auditRemark')
    rawJsonBase64 = validator.validate_not_empty(params, 'rawJson')
    rawJson = base64.base64ToString(rawJsonBase64)
    auditor = value.safe_get_in_key(params, 'auditor')
    uploadTime = datetime.datetime.now()
    if auditor == None:
        auditor = operator.name
    passCount = 0
    doneCount = 0
    ngCount = 0
    totalCount = 0
    audit_items = []
    if rawJson != None and rawJson != '':
        audit_items = json.loads(rawJson)
        for e in audit_items:
            totalCount += 1
            status = value.safe_get_in_key(e, 'status')
            if status != None:
                doneCount += 1
                if status == 'NG':
                    ngCount += 1
                elif status == 'OK':
                    passCount += 1

    entry = MDEAuditItem(lob=lob, site=site, productLine=productLine, project=project, part=part,
                         beginTime=beginTime, endTime=endTime, uploadTime=uploadTime, passCount=passCount, ngCount=ngCount, doneCount=doneCount, totalCount=totalCount, createTime=datetime.datetime.now(),
                         auditorId=operator.id, auditor=auditor)
    entry.save()
    if audit_items != None and len(audit_items) > 0:
        audit_item_check_item._batch_add_check_items(entry.id, lob, site, productLine, project, part, operator.id, auditor, uploadTime, audit_items)
    return response.ResponseData({
        'id': entry.id
    })
