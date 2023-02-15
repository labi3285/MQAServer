import sys, os
from django.forms.models import model_to_dict
from django.db.models import Q
from django.db import models

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

from aws_mqaserver.team_Display.models import DisplayCheckType
from aws_mqaserver.team_Display.models import DisplayCheckListItemEnclosure

import json

logger = logging.getLogger('django')

# Get Check List Items
def get_check_list_items(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    checkListId = validator.validate_not_empty(params, 'checkListId')
    try:
        list = DisplayCheckListItemEnclosure.objects.all().filter(checkListId=checkListId).order_by("sn")
        if list is None:
            return response.ResponseData([])
        arr = []
        for e in list:
            arr.append(model_to_dict(e))
        return response.ResponseData(arr)
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')

# Get Check List Items Page
def get_check_list_items_page(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    pageNum = validator.validate_not_empty(params, 'pageNum')
    pageSize = validator.validate_not_empty(params, 'pageSize')
    checkListId = validator.validate_not_empty(params, 'checkListId')
    try:
        list = DisplayCheckListItemEnclosure.objects.all().filter(checkListId=checkListId).order_by("sn")
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

def _batch_delete_check_list_items(checkListId):
    list = DisplayCheckListItemEnclosure.objects.filter(checkListId=checkListId)
    for e in list:
        e.delete()

def _batch_add_check_list_items(checkListId, type, dicArr):
    batch = []
    for e in dicArr:
        sn = validator.validate_integer(e, 'SN')
        area = value.safe_get_in_key(e, 'Area', '')
        mainProcess = validator.validate_not_empty_in_keys(e, ['Main process', 'Process'])
        subProcess = validator.validate_not_empty_in_keys(e, ['Sub process (Station/Process description)', 'Sub-Process/Section'])
        checkItems = validator.validate_not_empty(e, 'Check Items')
        samplingSize = value.safe_get_in_key(e, 'Sampling Size', '')
        lookingFor = value.safe_get_in_keys(e, ['Looking For', 'Looking-for'], '')
        recordsFindings = value.safe_get_in_key(e, ['Records Findings', 'Records/Findings'], '')
        result = value.safe_get_in_key(e, 'Result', '')
        auditSampleSize = value.safe_get_in_key(e, 'Audit Sample Size', '')
        disScore = value.safe_get_in_key(e, 'DIS Score')
        disTimes = value.safe_get_in_key(e, 'Times')
        skip = value.safe_get_bool_in_key(e, 'Skip')
        item = DisplayCheckListItemEnclosure(
            checkListId=checkListId,
            sn=sn,
            area=area,
            mainProcess=mainProcess,
            subProcess=subProcess,
            checkItems=checkItems,
            samplingSize=samplingSize,
            lookingFor=lookingFor,
            recordsFindings=recordsFindings,
            result=result,
            auditSampleSize=auditSampleSize,
            disScore=disScore,
            disTimes=disTimes,
            skip=skip,
            )
        batch.append(item)
    DisplayCheckListItemEnclosure.objects.bulk_create(batch, batch_size=len(batch))

