
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

from aws_mqaserver.models import CheckType
from aws_mqaserver.models import CheckListItemModule
from aws_mqaserver.models import CheckListItemEnclosure
from aws_mqaserver.models import CheckListItemORT
from aws_mqaserver.models import CheckListItemGlue
from aws_mqaserver.models import CheckListItemDestructive

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
        if type == CheckType.Module:
            list = CheckListItemModule.objects.all().filter(checkListId=checkListId).order_by("sn")
        elif type == CheckType.Enclosure:
            list = CheckListItemEnclosure.objects.all().filter(checkListId=checkListId).order_by("sn")
        elif type == CheckType.ORT:
            list = CheckListItemORT.objects.all().filter(checkListId=checkListId).order_by("sn")
        elif type == CheckType.Glue:
            list = CheckListItemGlue.objects.all().filter(checkListId=checkListId).order_by("sn")
        elif type == CheckType.Destructive:
            list = CheckListItemDestructive.objects.all().filter(checkListId=checkListId).order_by("sn")
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
        if type == CheckType.Module:
            list = CheckListItemModule.objects.all().filter(checkListId=checkListId).order_by("sn")
        elif type == CheckType.Enclosure:
            list = CheckListItemEnclosure.objects.all().filter(checkListId=checkListId).order_by("sn")
        elif type == CheckType.ORT:
            list = CheckListItemORT.objects.all().filter(checkListId=checkListId).order_by("sn")
        elif type == CheckType.Glue:
            list = CheckListItemGlue.objects.all().filter(checkListId=checkListId).order_by("sn")
        elif type == CheckType.Destructive:
            list = CheckListItemDestructive.objects.all().filter(checkListId=checkListId).order_by("sn")
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
    if type == CheckType.Module:
        list = CheckListItemModule.objects.filter(checkListId=checkListId)
        for e in list:
            e.delete()        
    elif type == CheckType.Enclosure:
        list = CheckListItemEnclosure.objects.filter(checkListId=checkListId)
        for e in list:
            e.delete()
    elif type == CheckType.ORT:
        list = CheckListItemORT.objects.filter(checkListId=checkListId)
        for e in list:
            e.delete()
    elif type == CheckType.Glue:
        list = CheckListItemGlue.objects.filter(checkListId=checkListId)
        for e in list:
            e.delete()
    elif type == CheckType.Destructive:
        list = CheckListItemDestructive.objects.filter(checkListId=checkListId)
        for e in list:
            e.delete()

def _batch_add_check_list_items(checkListId, team, type, dicArr):
    if type == CheckType.Module:
        batch = []
        for e in dicArr:
            sn = validator.validate_integer(e, 'SN')
            mainProcess = validator.validate_not_empty(e, 'Main process')
            subProcess = validator.validate_not_empty(e, 'Sub process (Station/Process description)')
            ifCtq = value.safe_get_in_key(e, 'IF CTQ', '')
            if ifCtq == 'N':
                ifCtq = False
            else:
                ifCtq = True
            measurementEquipment = value.safe_get_in_key(e, 'Measurement Equipment', '')
            LSL = value.safe_get_in_key(e, 'LSL', '')
            USL = value.safe_get_in_key(e, 'USL', '')
            LCL = value.safe_get_in_key(e, 'LCL (optional)', '')
            UCL = value.safe_get_in_key(e, 'UCL (optional)', '')
            checkItem = value.safe_get_in_key(e, 'Characteristic (Check item)', '')
            checkResult = value.safe_get_in_key(e, 'Result (Record check result)', '')
            sampleUnit = value.safe_get_in_key(e, 'Sample Unit', '')
            sampleSize = value.safe_get_in_key(e, 'Sample Size', '')
            frenquencyBasis = value.safe_get_in_key(e, 'Frenquency/Basis', '')
            controlType = value.safe_get_in_key(e, 'Control Type', '')
            controlMethod = value.safe_get_in_key(e, 'Control Method', '')
            controlCriteria = value.safe_get_in_key(e, 'Control Criteria', '')
            responsePlan = value.safe_get_in_key(e, 'Response plan', '')
            sopNo = value.safe_get_in_key(e, 'SOP-NO.', '')
            result = value.safe_get_in_key(e, 'Result (Verify Vendors execution)OK/NG', '')
            item = CheckListItemModule(
                checkListId=checkListId,
                team=team,
                sn=sn,
                mainProcess=mainProcess,
                subProcess=subProcess,
                ifCtq=ifCtq,
                measurementEquipment=measurementEquipment,
                LSL=LSL,
                USL=USL,
                LCL=LCL,
                UCL=UCL,
                checkItem=checkItem,
                checkResult=checkResult,
                sampleUnit=sampleUnit,
                sampleSize=sampleSize,
                frenquencyBasis=frenquencyBasis,
                controlType=controlType,
                controlMethod=controlMethod,
                controlCriteria=controlCriteria,
                responsePlan=responsePlan,
                sopNo=sopNo,
                result=result,
                )
            batch.append(item)
        CheckListItemModule.objects.bulk_create(batch, batch_size=len(batch))    
    elif type == CheckType.Enclosure:
        batch = []
        for e in dicArr:
            sn = validator.validate_integer(e, 'SN')
            area = validator.validate_not_empty(e, 'Area')
            mainProcess = validator.validate_not_empty_in_keys(e, ['Main process', 'Process'])
            subProcess = validator.validate_not_empty_in_keys(e, ['Sub process (Station/Process description)', 'Sub-Process/Section'])
            checkItems = validator.validate_not_empty(e, 'Check Items')
            samplingSize = value.safe_get_in_key(e, 'Sampling Size', '')
            lookingFor = value.safe_get_in_keys(e, ['Looking For', 'Looking-for'], '')
            recordsFindings = value.safe_get_in_key(e, ['Records Findings', 'Records/Findings'], '')
            result = value.safe_get_in_key(e, 'Result', '')
            item = CheckListItemEnclosure(
                checkListId=checkListId,
                team=team,
                sn=sn,
                area=area,
                mainProcess=mainProcess,
                subProcess=subProcess,
                checkItems=checkItems,
                samplingSize=samplingSize,
                lookingFor=lookingFor,
                recordsFindings=recordsFindings,
                result=result,
                )
            batch.append(item)
        CheckListItemEnclosure.objects.bulk_create(batch, batch_size=len(batch))
    elif type == CheckType.ORT:
        batch = []
        for e in dicArr:
            sn = validator.validate_integer(e, 'SN')
            project = validator.validate_not_empty(e, 'Project')
            testItem = validator.validate_not_empty(e, 'Test Item')
            testConditionParameter = value.safe_get_in_key(e, 'Test Condition/Parameter', '')
            equipment = value.safe_get_in_key(e, 'Equipment', '')
            fixtureYN = value.safe_get_in_key(e, 'Fixture (Y/N)', '')
            sampleOrientation = value.safe_get_in_key(e, 'Sample Orientation', '')
            recoveryTime = value.safe_get_in_key(e, 'Recovery Time', '')
            sampleSize = value.safe_get_in_key(e, 'Sample Size', '')
            samplingFreq = value.safe_get_in_key(e, 'Sampling Freq.', '')
            duration = value.safe_get_in_key(e, 'Duration', '')
            readPoint = value.safe_get_in_key(e, 'Read Point', '')
            passFailCriteria = value.safe_get_in_key(e, 'Pass/Fail Criteria', '')
            OCAP = value.safe_get_in_key(e, 'OCAP', '')
            result = value.safe_get_in_key(e, 'Result (Verify Vendors execution)OK/NG', '')
            item = CheckListItemORT(
                checkListId=checkListId,
                team=team,
                sn=sn,
                project=project,
                testItem=testItem,
                testConditionParameter=testConditionParameter,
                equipment=equipment,
                fixtureYN=fixtureYN,
                sampleOrientation=sampleOrientation,
                recoveryTime=recoveryTime,
                sampleSize=sampleSize,
                samplingFreq=samplingFreq,
                duration=duration,
                readPoint=readPoint,
                passFailCriteria=passFailCriteria,
                OCAP=OCAP,
                result=result,
                )
            batch.append(item)
        if len(batch) > 0:
            CheckListItemORT.objects.bulk_create(batch, batch_size=len(batch))

    elif type == CheckType.Glue:
        batch = []
        for e in dicArr:
            sn = validator.validate_not_empty(e, 'SN')
            theClass = validator.validate_not_empty(e, 'Class')
            lineShift = validator.validate_not_empty(e, 'Line&Shift')
            projects = validator.validate_not_empty(e, 'Projects')
            item = validator.validate_not_empty(e, 'Item')
            unit = validator.validate_not_empty(e, 'Unit')
            glue = validator.validate_not_empty(e, 'Glue')
            LSL = validator.validate_not_empty(e, 'LSL')
            USL = validator.validate_not_empty(e, 'USL')
            item = CheckListItemGlue(
                checkListId=checkListId,
                team=team,
                sn=sn,
                theClass=theClass,
                lineShift=lineShift,
                projects=projects,
                glue=glue,
                item=item,
                unit=unit,
                LSL=LSL,
                USL=USL,
                )
            batch.append(item)
        if len(batch) > 0:
            CheckListItemGlue.objects.bulk_create(batch, batch_size=len(batch))

    elif type == CheckType.Destructive:
        batch = []
        for e in dicArr:
            sn = validator.validate_not_empty(e, 'SN')
            theClass = validator.validate_not_empty(e, 'Class')
            lineShift = validator.validate_not_empty(e, 'Line&Shift')
            projects = validator.validate_not_empty(e, 'Projects')
            item = validator.validate_not_empty(e, 'Item')
            unit = validator.validate_not_empty(e, 'Unit')
            LSL = validator.validate_not_empty(e, 'LSL')
            item = CheckListItemDestructive(
                checkListId=checkListId,
                team=team,
                sn=sn,
                theClass=theClass,
                lineShift=lineShift,
                projects=projects,
                item=item,
                unit=unit,
                LSL=LSL,
                )
            batch.append(item)
        if len(batch) > 0:
            CheckListItemDestructive.objects.bulk_create(batch, batch_size=len(batch))