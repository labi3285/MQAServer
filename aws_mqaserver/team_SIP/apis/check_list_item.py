import sys, os
from django.forms.models import model_to_dict
from django.db.models import Q
from django.db import models

from io import BytesIO
import pandas
from django.core.files import temp as tempfile

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

from aws_mqaserver.team_SIP.models import SIPCheckType
from aws_mqaserver.team_SIP.models import SIPCheckList
from aws_mqaserver.team_SIP.models import SIPCheckListItemEnclosure

import json

logger = logging.getLogger('django')

# Get Check List Items
def get_check_list_items(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    checkListId = validator.validate_not_empty(params, 'checkListId')
    type = validator.validate_not_empty(params, 'type')
    try:
        list = None
        if type == SIPCheckType.Enclosure:
            list = SIPCheckListItemEnclosure.objects.all().filter(checkListId=checkListId).order_by("sn")
        if list is None:
            return response.ResponseData([])
        arr = []
        for e in list:
            arr.append(model_to_dict(e))
        return response.ResponseData(arr)
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')

# Export Check List Items
def export_check_list_items(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    checkListId = validator.validate_not_empty(params, 'checkListId')
    try:
        list = SIPCheckListItemEnclosure.objects.all().filter(checkListId=checkListId).order_by("sn")
        arr = []
        if list is None or len(list) == 0:
            return response.ResponseError('Check List Empty')
        entry = SIPCheckList.objects.get(id=checkListId)
        excel_name = entry.lob + '_' + entry.site + '_' + entry.productLine + '_' + entry.project + '_' + entry.part + '.xlsx'
        output = BytesIO()
        excel_writer = pandas.ExcelWriter(output, engine="xlsxwriter")
        excel_row = []
        for e in list:
            excel_row.append([
                e.sn,
                e.area,
                e.mainProcess,
                e.subProcess,
                e.checkItems,
                e.samplingSize,
                e.lookingFor,
            ])
        pandas.DataFrame(excel_row, columns=[
            'SN', 'Area', 'Main process', 'Sub process (Station/Process description)', 'Check Items', 'Sampling Size', 'Looking For'
        ]).to_excel(excel_writer, sheet_name='Check List', index=False)
        excel_writer.close()
        output.seek(0)
        return response.HttpResponseExcel(output.getvalue(), excel_name)
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
    type = validator.validate_not_empty(params, 'type')
    try:
        list = None
        if type == SIPCheckType.Enclosure:
            list = SIPCheckListItemEnclosure.objects.all().filter(checkListId=checkListId).order_by("sn")
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

def _batch_delete_check_list_items(checkListId, type):
    if type == SIPCheckType.Enclosure:
        list = SIPCheckListItemEnclosure.objects.filter(checkListId=checkListId)
        for e in list:
            e.delete()

def _batch_add_check_list_items(checkListId, type, dicArr):
    if type == SIPCheckType.Enclosure:
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
            item = SIPCheckListItemEnclosure(
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
        SIPCheckListItemEnclosure.objects.bulk_create(batch, batch_size=len(batch))

