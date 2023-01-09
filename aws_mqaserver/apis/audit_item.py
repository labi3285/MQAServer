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

from aws_mqaserver.models import AuditItem
from aws_mqaserver.apis import mil_item

import json

logger = logging.getLogger('django')

@transaction.atomic
def upload_audit_item(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    team = validator.get_team(params, operator)
    lob = validator.validate_not_empty(params, 'lob')
    site = validator.validate_not_empty(params, 'site')
    productLine = validator.validate_not_empty(params, 'productLine')
    project = validator.validate_not_empty(params, 'project')
    part = validator.validate_not_empty(params, 'part')
    type = validator.validate_integer(params, 'type')
    beginTime = validator.validate_date(params, 'beginTime')
    endTime = validator.validate_date(params, 'endTime')
    rawJsonBase64 = validator.validate_not_empty(params, 'rawJson')
    rawJson = base64.base64ToString(rawJsonBase64)
    auditor = value.safe_get_in_key(params, 'auditor')
    uploadTime = datetime.datetime.now()
    if auditor == None:
        auditor = operator.name
    passCount = 0
    failCount = 0
    doneCount = 0
    totalCount = 0
    findingCount = 0
    findingsArr = None
    if rawJson != None and rawJson != '':
        arr = json.loads(rawJson)
        findingsArr = []
        for e in arr:
            totalCount += 1
            isDone = value.safe_get_in_key(e, 'isDone', False)
            if isDone:
                doneCount += 1
            findings = value.safe_get_in_key(e, 'findings')
            if findings != None and len(findings) > 0:
                failCount += 1
                for f in findings:
                    findingCount += 1
                    findingsArr.append(f)
            else:
                if isDone:
                    passCount += 1
    entry = AuditItem(team=team, lob=lob, site=site, productLine=productLine, project=project, part=part, type=type,
                        beginTime=beginTime, endTime=endTime, uploadTime=uploadTime, passCount=passCount, failCount=failCount, doneCount=doneCount, totalCount=totalCount, findingCount=findingCount, rawJson=rawJson, createTime=datetime.datetime.now(),
                          auditorId=operator.id, auditor=auditor)
    entry.save()
    if findingsArr != None and len(findingsArr) > 0:
        mil_item._batch_add_mil_items(entry.id, team, lob, site, productLine, project, part, type, operator.id,
                                      auditor, findingsArr)
        return response.ResponseData({
            'id': entry.id
        })
    else:
        return response.ResponseData({
            'id': entry.id
        })