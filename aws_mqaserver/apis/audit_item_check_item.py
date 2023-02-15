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

from aws_mqaserver.models import CheckType
from aws_mqaserver.models import AuditItemCheckItemModule
from aws_mqaserver.models import AuditItemCheckItemEnclosure
from aws_mqaserver.models import AuditItemCheckItemORT

import json

logger = logging.getLogger('django')

# Get Audit Check Items Page
def get_audit_item_check_items_page_module(request):
    return _get_audit_item_check_items_page(request, 'Module')
def _get_audit_item_check_items_page(request, type):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    pageNum = validator.validate_not_empty(params, 'pageNum')
    pageSize = validator.validate_not_empty(params, 'pageSize')
    auditItemId = validator.validate_not_empty(params, 'auditItemId')
    try:
        list = None
        if type == CheckType.Module:
            list = AuditItemCheckItemModule.objects.all().filter(auditItemId=auditItemId).order_by("sn")
        elif type == CheckType.Enclosure:
            list = AuditItemCheckItemEnclosure.objects.all().filter(auditItemId=auditItemId).order_by("sn")
        elif type == CheckType.ORT:
            list = AuditItemCheckItemORT.objects.all().filter(auditItemId=auditItemId).order_by("sn")
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
    if type == CheckType.Module:
        for e in dicArr:
            check_item = e['checkItem']
            checkListId = value.safe_get_in_key(check_item, 'checkListId')
            checkItem_sn = value.safe_get_in_key(check_item, 'sn')
            checkItem_mainProcess = value.safe_get_in_key(check_item, 'mainProcess', '')
            checkItem_subProcess = value.safe_get_in_key(check_item, 'subProcess', '')
            checkItem_ifCtq = value.safe_get_in_key(check_item, 'ifCtq', True)
            checkItem_measurementEquipment = value.safe_get_in_key(check_item, 'measurementEquipment', '')
            checkItem_LSL = value.safe_get_in_key(check_item, 'LSL', '')
            checkItem_USL = value.safe_get_in_key(check_item, 'USL', '')
            checkItem_LCL = value.safe_get_in_key(check_item, 'LCL', '')
            checkItem_UCL = value.safe_get_in_key(check_item, 'UCL', '')
            checkItem_checkItem = value.safe_get_in_key(check_item, 'checkItem', '')
            checkItem_sampleUnit = value.safe_get_in_key(check_item, 'sampleUnit', '')
            checkItem_sampleSize = value.safe_get_in_key(check_item, 'sampleSize', '')
            checkItem_frenquencyBasis = value.safe_get_in_key(check_item, 'frenquencyBasis', '')
            checkItem_controlType = value.safe_get_in_key(check_item, 'controlType', '')
            checkItem_controlMethod = value.safe_get_in_key(check_item, 'controlMethod', '')
            checkItem_controlCriteria = value.safe_get_in_key(check_item, 'controlCriteria', '')
            checkItem_responsePlan = value.safe_get_in_key(check_item, 'responsePlan', '')
            checkItem_sopNo = value.safe_get_in_key(check_item, 'sopNo', '')
            checkItem_auditSampleSize = value.safe_get_in_key(check_item, 'auditSampleSize', '')
            checkItem_disScore = value.safe_get_in_key(check_item, 'disScore')
            checkItem_disTimes = value.safe_get_in_key(check_item, 'disTimes')
            checkItem_skip = value.safe_get_bool_in_key(check_item, 'skip')
            checkResult = value.safe_get_in_key(e, 'checkResult')
            peopleTrain = value.safe_get_in_key(e, 'peopleTrain')
            machineMaintenance = value.safe_get_in_key(e, 'machineMaintenance')
            onsiteVerify = value.safe_get_in_key(e, 'onsiteVerify')
            materialHandling = value.safe_get_in_key(e, 'materialHandling')
            environmentSetting = value.safe_get_in_key(e, 'environmentSetting')
            workshopLineMachine = value.safe_get_in_key(e, 'workshopLineMachine')
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
            item = AuditItemCheckItemModule(
                auditItemId=auditItemId,
                lob=lob,
                site=site,
                productLine=productLine,
                project=project,
                part=part,
                checkListId=checkListId,
                checkItem_sn=checkItem_sn,
                checkItem_mainProcess=checkItem_mainProcess,
                checkItem_subProcess=checkItem_subProcess,
                checkItem_ifCtq=checkItem_ifCtq,
                checkItem_measurementEquipment=checkItem_measurementEquipment,
                checkItem_LSL=checkItem_LSL,
                checkItem_USL=checkItem_USL,
                checkItem_LCL=checkItem_LCL,
                checkItem_UCL=checkItem_UCL,
                checkItem_checkItem=checkItem_checkItem,
                checkItem_sampleUnit=checkItem_sampleUnit,
                checkItem_sampleSize=checkItem_sampleSize,
                checkItem_frenquencyBasis=checkItem_frenquencyBasis,
                checkItem_controlType=checkItem_controlType,
                checkItem_controlMethod=checkItem_controlMethod,
                checkItem_controlCriteria=checkItem_controlCriteria,
                checkItem_responsePlan=checkItem_responsePlan,
                checkItem_sopNo=checkItem_sopNo,
                checkItem_auditSampleSize=checkItem_auditSampleSize,
                checkItem_disScore=checkItem_disScore,
                checkItem_disTimes=checkItem_disTimes,
                checkItem_skip=checkItem_skip,
                peopleTrain=peopleTrain,
                machineMaintenance=machineMaintenance,
                onsiteVerify=onsiteVerify,
                materialHandling=materialHandling,
                environmentSetting=environmentSetting,
                workshopLineMachine=workshopLineMachine,
                checkResult=checkResult,
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
            AuditItemCheckItemModule.objects.bulk_create(batch, batch_size=len(batch))

    elif type == CheckType.Enclosure:
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
            checkItem_skip = value.safe_get_bool_in_key(check_item, 'skip')
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
            item = AuditItemCheckItemEnclosure(
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
            AuditItemCheckItemEnclosure.objects.bulk_create(batch, batch_size=len(batch))

    elif type == CheckType.ORT:
        for e in dicArr:
            check_item = e['checkItem']
            checkListId = value.safe_get_in_key(check_item, 'checkListId')
            checkItem_sn = value.safe_get_in_key(check_item, 'sn')
            checkItem_project = value.safe_get_in_key(check_item, 'project')
            checkItem_testItem = value.safe_get_in_key(check_item, 'testItem')
            checkItem_testConditionParameter = value.safe_get_in_key(check_item, 'testConditionParameter')
            checkItem_equipment = value.safe_get_in_key(check_item, 'equipment')
            checkItem_fixtureYN = value.safe_get_in_key(check_item, 'fixtureYN')
            checkItem_sampleOrientation = value.safe_get_in_key(check_item, 'sampleOrientation')
            checkItem_recoveryTime = value.safe_get_in_key(check_item, 'recoveryTime')
            checkItem_sampleSize = value.safe_get_in_key(check_item, 'sampleSize')
            checkItem_samplingFreq = value.safe_get_in_key(check_item, 'samplingFreq')
            checkItem_duration = value.safe_get_in_key(check_item, 'duration')
            checkItem_readPoint = value.safe_get_in_key(check_item, 'readPoint')
            checkItem_passFailCriteria = value.safe_get_in_key(check_item, 'passFailCriteria')
            checkItem_OCAP = value.safe_get_in_key(check_item, 'OCAP')
            checkItem_disScore = value.safe_get_in_key(check_item, 'disScore')
            checkItem_disTimes = value.safe_get_in_key(check_item, 'disTimes')
            checkItem_skip = value.safe_get_bool_in_key(check_item, 'skip')
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
            item = AuditItemCheckItemORT(
                auditItemId=auditItemId,
                lob=lob,
                site=site,
                productLine=productLine,
                project=project,
                part=part,
                checkListId=checkListId,
                checkItem_sn=checkItem_sn,
                checkItem_project=checkItem_project,
                checkItem_testItem=checkItem_testItem,
                checkItem_testConditionParameter=checkItem_testConditionParameter,
                checkItem_equipment=checkItem_equipment,
                checkItem_fixtureYN=checkItem_fixtureYN,
                checkItem_sampleOrientation=checkItem_sampleOrientation,
                checkItem_recoveryTime=checkItem_recoveryTime,
                checkItem_sampleSize=checkItem_sampleSize,
                checkItem_samplingFreq=checkItem_samplingFreq,
                checkItem_duration=checkItem_duration,
                checkItem_readPoint=checkItem_readPoint,
                checkItem_passFailCriteria=checkItem_passFailCriteria,
                checkItem_OCAP=checkItem_OCAP,
                checkItem_disScore=checkItem_disScore,
                checkItem_disTimes=checkItem_disTimes,
                checkItem_skip=checkItem_skip,
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
            AuditItemCheckItemORT.objects.bulk_create(batch, batch_size=len(batch))