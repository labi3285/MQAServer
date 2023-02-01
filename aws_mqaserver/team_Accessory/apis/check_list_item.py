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

from aws_mqaserver.team_Accessory.models import AccessoryCheckType
from aws_mqaserver.team_Accessory.models import AccessoryCheckListItemGlue
from aws_mqaserver.team_Accessory.models import AccessoryCheckListItemDestructive

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
        if type == AccessoryCheckType.Glue:
            list = AccessoryCheckListItemGlue.objects.all().filter(checkListId=checkListId).order_by("sn")
        elif type == AccessoryCheckType.Destructive:
            list = AccessoryCheckListItemDestructive.objects.all().filter(checkListId=checkListId).order_by("sn")
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
    type = validator.validate_not_empty(params, 'type')
    try:
        list = None
        if type == AccessoryCheckType.Glue:
            list = AccessoryCheckListItemGlue.objects.all().filter(checkListId=checkListId).order_by("sn")
        elif type == AccessoryCheckType.Destructive:
            list = AccessoryCheckListItemDestructive.objects.all().filter(checkListId=checkListId).order_by("sn")
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
    if type == AccessoryCheckType.Glue:
        list = AccessoryCheckListItemGlue.objects.filter(checkListId=checkListId)
        for e in list:
            e.delete()
    elif type == AccessoryCheckType.Destructive:
        list = AccessoryCheckListItemDestructive.objects.filter(checkListId=checkListId)
        for e in list:
            e.delete()

def _batch_add_check_list_items(checkListId, type, dicArr):
    if type == AccessoryCheckType.Glue:
        batch = []
        for e in dicArr:
            sn = validator.validate_not_empty(e, 'SN')
            site = validator.validate_not_empty(e, 'Site')
            theClass = validator.validate_not_empty(e, 'Class')
            lineShift = validator.validate_not_empty(e, 'Line&Shift')
            projects = validator.validate_not_empty(e, 'Projects')
            item = validator.validate_not_empty(e, 'Item')
            unit = validator.validate_not_empty(e, 'Unit')
            LSL = value.safe_get_in_key(e, 'LSL', '')
            USL = value.safe_get_in_key(e, 'USL', '')
            item = AccessoryCheckListItemGlue(
                checkListId=checkListId,
                sn=sn,
                site=site,
                theClass=theClass,
                lineShift=lineShift,
                projects=projects,
                item=item,
                unit=unit,
                LSL=LSL,
                USL=USL,
                )
            batch.append(item)
        if len(batch) > 0:
            AccessoryCheckListItemGlue.objects.bulk_create(batch, batch_size=len(batch))

    elif type == AccessoryCheckType.Destructive:
        batch = []
        for e in dicArr:
            sn = validator.validate_not_empty(e, 'SN')
            site = validator.validate_not_empty(e, 'Site')
            theClass = validator.validate_not_empty(e, 'Class')
            lineShift = validator.validate_not_empty(e, 'Line&Shift')
            projects = validator.validate_not_empty(e, 'Projects')
            item = validator.validate_not_empty(e, 'Item')
            unit = validator.validate_not_empty(e, 'Unit')
            LSL = value.safe_get_in_key(e, 'LSL', '')
            USL = value.safe_get_in_key(e, 'USL', '')
            item = AccessoryCheckListItemDestructive(
                checkListId=checkListId,
                sn=sn,
                site=site,
                theClass=theClass,
                lineShift=lineShift,
                projects=projects,
                item=item,
                unit=unit,
                LSL=LSL,
                USL=USL,
                )
            batch.append(item)
        if len(batch) > 0:
            AccessoryCheckListItemDestructive.objects.bulk_create(batch, batch_size=len(batch))
