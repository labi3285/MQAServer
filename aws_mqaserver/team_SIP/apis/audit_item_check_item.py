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

from aws_mqaserver.team_SIP.models import SIPCheckType
from aws_mqaserver.team_SIP.models import SIPAuditItemCheckItemEnclosure

import json

logger = logging.getLogger('django')

# Get Audit Check Items Page
def get_audit_item_check_items_page_enclosure(request):
    return _get_audit_item_check_items_page(request, 'Enclosure')
def _get_audit_item_check_items_page(request, type):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    pageNum = validator.validate_not_empty(params, 'pageNum')
    pageSize = validator.validate_not_empty(params, 'pageSize')
    auditItemId = validator.validate_not_empty(params, 'auditItemId')
    try:
        list = None
        if type == SIPCheckType.Enclosure:
            list = SIPAuditItemCheckItemEnclosure.objects.all().filter(auditItemId=auditItemId).order_by("sn")
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
    if type == SIPCheckType.Enclosure:
        for e in dicArr:
            check_item = e['checkItem']
            checkListId = value.safe_get_in_key(check_item, 'checkListId')
            checkItem_sn = value.safe_get_in_key(check_item, 'sn')
            checkItem_area = value.safe_get_in_key(check_item, 'area', '')
            checkItem_mainProcess = value.safe_get_in_key(check_item, 'mainProcess', '')
            checkItem_subProcess = value.safe_get_in_key(check_item, 'subProcess', '')
            checkItem_checkItems = value.safe_get_in_key(check_item, 'checkItems', '')
            checkItem_samplingSize = value.safe_get_in_key(check_item, 'samplingSize', '')
            checkItem_lookingFor = value.safe_get_in_key(check_item, 'lookingFor', '')
            checkItem_recordsFindings = value.safe_get_in_key(check_item, 'recordsFindings', '')
            checkItem_auditSampleSize = value.safe_get_in_key(check_item, 'auditSampleSize', '')
            checkItem_disScore = value.safe_get_in_key(check_item, 'disScore')
            checkItem_disTimes = value.safe_get_in_key(check_item, 'disTimes')
            checkItem_skip = value.safe_get_in_key(check_item, 'skip')
            records = value.safe_get_in_key(e, 'records')
            result = value.safe_get_in_key(e, 'result')
            findings_json = None
            findings = value.safe_get_in_key(e, 'findings')
            if findings != None:
                findings_json = json.dumps(findings)
            hasFindings = value.safe_get_in_key(e, 'hasFindings', False)
            isSkip = value.safe_get_bool_in_key(e, 'isSkip', False)
            isDone = value.safe_get_bool_in_key(e, 'isDone', False)
            status = value.safe_get_in_key(e, 'status')
            createTime = value.safe_get_date_in_key(e, 'createTime')
            item = SIPAuditItemCheckItemEnclosure(
                auditItemId=auditItemId,
                lob=lob,
                site=site,
                productLine=productLine,
                project=project,
                part=part,
                checkListId=checkListId,
                checkItem_sn=checkItem_sn,
                checkItem_area=checkItem_area,
                checkItem_mainProcess=checkItem_mainProcess,
                checkItem_subProcess=checkItem_subProcess,
                checkItem_checkItems=checkItem_checkItems,
                checkItem_samplingSize=checkItem_samplingSize,
                checkItem_lookingFor=checkItem_lookingFor,
                checkItem_recordsFindings=checkItem_recordsFindings,
                checkItem_auditSampleSize=checkItem_auditSampleSize,
                checkItem_disScore=checkItem_disScore,
                checkItem_disTimes=checkItem_disTimes,
                checkItem_skip=checkItem_skip,
                records=records,
                result=result,
                hasFindings=hasFindings,
                findings=findings_json,
                isSkip=isSkip,
                isDone=isDone,
                status=status,
                createTime=createTime,
                uploadTime=uploadTime,
                auditorId=auditorId,
                auditor=auditor,
            )
            batch.append(item)
        if len(batch) > 0:
            SIPAuditItemCheckItemEnclosure.objects.bulk_create(batch, batch_size=len(batch))

