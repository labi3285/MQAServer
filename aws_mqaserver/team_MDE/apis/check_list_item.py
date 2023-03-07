import sys, os
from django.forms.models import model_to_dict
from django.db.models import Q
from django.db import models
from django.http import HttpResponse, HttpRequest

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

from aws_mqaserver.team_MDE.models import MDECheckList
from aws_mqaserver.team_MDE.models import MDECheckListItem

import json

logger = logging.getLogger('django')


# Get Check List Items
def get_check_list_items(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    checkListId = validator.validate_not_empty(params, 'checkListId')
    try:
        list = MDECheckListItem.objects.all().filter(checkListId=checkListId).order_by("sn")
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
        list = MDECheckListItem.objects.all().filter(checkListId=checkListId).order_by("sn")
        arr = []
        if list is None or len(list) == 0:
            return response.ResponseError('Check List Empty')
        entry = MDECheckList.objects.get(id=checkListId)
        excel_name = entry.lob + '_' + entry.site + '_' + entry.productLine + '_' + entry.project + '.xlsx'
        output = BytesIO()
        excel_writer = pandas.ExcelWriter(output, engine="xlsxwriter")
        excel_row = []
        for e in list:
            excel_row.append([
                e.sn,
                e.station,
                e.process,
                e.productLine,
                e.project,
                e.checkItem,
                e.USL,
                e.LSL
            ])
        pandas.DataFrame(excel_row, columns=[
            'SN', 'Station', 'Process', 'Product line', 'Project', 'Check Item', 'USL', 'LSL'
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
    try:
        list = MDECheckListItem.objects.all().filter(checkListId=checkListId).order_by("sn")
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
    list = MDECheckListItem.objects.filter(checkListId=checkListId)
    for e in list:
        e.delete()


def _batch_add_check_list_items(checkListId, dicArr):
    batch = []
    for e in dicArr:
        sn = validator.validate_not_empty(e, 'SN')
        station = validator.validate_not_empty(e, 'Station')
        process = validator.validate_not_empty(e, 'Process')
        productLine = validator.validate_not_empty(e, 'Product line')
        project = validator.validate_not_empty(e, 'Project')
        checkItem = validator.validate_not_empty(e, 'Check Item')
        USL = value.safe_get_in_key(e, 'USL', 0)
        LSL = value.safe_get_in_key(e, 'LSL', 0)
        item = MDECheckListItem(
            checkListId=checkListId,
            sn=sn,
            station=station,
            process=process,
            productLine=productLine,
            project=project,
            checkItem=checkItem,
            LSL=LSL,
            USL=USL,
        )
        batch.append(item)
    if len(batch) > 0:
        MDECheckListItem.objects.bulk_create(batch, batch_size=len(batch))
