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
import math

from aws_mqaserver.utils import value
from aws_mqaserver.utils import validator
from aws_mqaserver.utils import response
from aws_mqaserver.utils import token
from aws_mqaserver.utils import ids

from aws_mqaserver.utils import audit

from aws_mqaserver.models import CheckType
from aws_mqaserver.models import CheckList
from aws_mqaserver.models import CheckListItemModule
from aws_mqaserver.models import CheckListItemEnclosure
from aws_mqaserver.models import CheckListItemORT

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
    type = validator.validate_not_empty(params, 'type')
    try:
        list = None
        if type == CheckType.Module:
            list = CheckListItemModule.objects.all().filter(checkListId=checkListId).order_by("sn")
        elif type == CheckType.Enclosure:
            list = CheckListItemEnclosure.objects.all().filter(checkListId=checkListId).order_by("sn")
        elif type == CheckType.ORT:
            list = CheckListItemORT.objects.all().filter(checkListId=checkListId).order_by("sn")
        arr = []
        if list is None or len(list) == 0:
            return response.ResponseError('Check List Empty')
        entry = CheckList.objects.get(id=checkListId)
        excel_name = entry.lob + '_' + entry.site + '_' + entry.productLine + '_' + entry.project + '_' + entry.part + '_' + type + '.xlsx'
        output = BytesIO()
        excel_writer = pandas.ExcelWriter(output, engine="xlsxwriter")
        excel_row = []
        if type == CheckType.Module:
            for e in list:
                ifCtq = ''
                if e.ifCtq:
                    ifCtq = 'Y'
                else:
                    ifCtq = 'N'

                excel_row.append([
                    e.sn,
                    e.mainProcess,
                    e.subProcess,
                    ifCtq,
                    e.measurementEquipment,
                    e.LSL,
                    e.USL,
                    e.LCL,
                    e.UCL,
                    e.checkItem,
                    e.sampleUnit,
                    e.sampleSize,
                    e.frenquencyBasis,
                    e.controlType,
                    e.controlMethod,
                    e.controlCriteria,
                    e.responsePlan,
                    e.sopNo,
                    e.auditSampleSize,
                ])
            pandas.DataFrame(excel_row, columns=[
                'SN', 'Main process', 'Sub process (Station/Process description)', 'IF CTQ', 'Measurement Equipment', 'LSL', 'USL', 'LCL (optional)', 'UCL (optional)',
                'Characteristic (Check item)', 'Sample Unit', 'Sample Size', 'Frenquency/Basis', 'Control Type', 'Control Method', 'Control Criteria', 'Response plan', 'SOP-NO.', 'Audit Sample Size'
            ]).to_excel(excel_writer, sheet_name='Check List', index=False)
        elif type == CheckType.Enclosure:
            for e in list:
                excel_row.append([
                    e.sn,
                    e.mainProcess,
                    e.subProcess,
                    e.checkItems,
                    e.samplingSize,
                ])
            pandas.DataFrame(excel_row, columns=[
                'SN', 'Main process', 'Sub process (Station/Process description)', 'Check Items', 'Sampling Size'
            ]).to_excel(excel_writer, sheet_name='Check List', index=False)
        elif type == CheckType.ORT:
            for e in list:
                excel_row.append([
                    e.sn,
                    e.project,
                    e.testItem,
                    e.testConditionParameter,
                    e.equipment,
                    e.fixtureYN,
                    e.sampleOrientation,
                    e.recoveryTime,
                    e.sampleSize,
                    e.samplingFreq,
                    e.duration,
                    e.readPoint,
                    e.passFailCriteria,
                    e.OCAP,
                ])
            pandas.DataFrame(excel_row, columns=[
                'SN', 'Project', 'Test Item', 'Test Condition/Parameter', 'Equipment', 'Fixture (Y/N)', 'Sample Orientation',
                'Recovery Time', 'Sample Size', 'Sampling Freq.', 'Duration', 'Read Point', 'Pass/Fail Criteria', 'OCAP'
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
        if type == CheckType.Module:
            list = CheckListItemModule.objects.all().filter(checkListId=checkListId).order_by("sn")
        elif type == CheckType.Enclosure:
            list = CheckListItemEnclosure.objects.all().filter(checkListId=checkListId).order_by("sn")
        elif type == CheckType.ORT:
            list = CheckListItemORT.objects.all().filter(checkListId=checkListId).order_by("sn")
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


def _batch_add_check_list_items(checkListId, type, dicArr):
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
            sampleUnit = value.safe_get_in_key(e, 'Sample Unit', '')
            sampleSize = value.safe_get_in_key(e, 'Sample Size', '')
            frenquencyBasis = value.safe_get_in_key(e, 'Frenquency/Basis', '')
            controlType = value.safe_get_in_key(e, 'Control Type', '')
            controlMethod = value.safe_get_in_key(e, 'Control Method', '')
            controlCriteria = value.safe_get_in_key(e, 'Control Criteria', '')
            responsePlan = value.safe_get_in_key(e, 'Response plan', '')
            sopNo = value.safe_get_in_key(e, 'SOP-NO.', '')
            auditSampleSize = value.safe_get_in_key(e, 'Audit Sample Size', '')
            disScore = value.safe_get_float_in_key(e, 'DIS Score')
            if disScore != None:
                disScore = int(math.ceil(disScore))
            realSampleSize = audit.get_real_sample_size(sampleSize, disScore)
            disTimes = value.safe_get_in_key(e, 'Times')
            skip = value.safe_get_bool_in_key(e, 'Skip')
            item = CheckListItemModule(
                checkListId=checkListId,
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
                sampleUnit=sampleUnit,
                sampleSize=sampleSize,
                realSampleSize=realSampleSize,
                frenquencyBasis=frenquencyBasis,
                controlType=controlType,
                controlMethod=controlMethod,
                controlCriteria=controlCriteria,
                responsePlan=responsePlan,
                sopNo=sopNo,
                auditSampleSize=auditSampleSize,
                disScore=disScore,
                disTimes=disTimes,
                skip=skip,
                )
            batch.append(item)
        CheckListItemModule.objects.bulk_create(batch, batch_size=len(batch))    
    elif type == CheckType.Enclosure:
        batch = []
        for e in dicArr:
            sn = validator.validate_integer(e, 'SN')
            area = value.safe_get_in_key(e, 'Area', '')
            mainProcess = validator.validate_not_empty_in_keys(e, ['Main process', 'Process'])
            subProcess = validator.validate_not_empty_in_keys(e, ['Sub process (Station/Process description)', 'Sub-Process/Section'])
            checkItems = value.safe_get_in_key(e, 'Check Items', '')
            samplingSize = value.safe_get_in_key(e, 'Sampling Size', '')
            lookingFor = value.safe_get_in_keys(e, ['Looking For', 'Looking-for'], '')
            recordsFindings = value.safe_get_in_key(e, ['Records Findings', 'Records/Findings'], '')
            result = value.safe_get_in_key(e, 'Result', '')
            auditSampleSize = value.safe_get_in_key(e, 'Audit Sample Size', '')
            disScore = value.safe_get_float_in_key(e, 'DIS Score')
            if disScore != None:
                disScore = int(math.ceil(disScore))
            realSampleSize = audit.get_real_sample_size(samplingSize, disScore)
            disTimes = value.safe_get_in_key(e, 'Times')
            skip = value.safe_get_bool_in_key(e, 'Skip')
            item = CheckListItemEnclosure(
                checkListId=checkListId,
                sn=sn,
                area=area,
                mainProcess=mainProcess,
                subProcess=subProcess,
                checkItems=checkItems,
                samplingSize=samplingSize,
                realSampleSize=realSampleSize,
                lookingFor=lookingFor,
                recordsFindings=recordsFindings,
                result=result,
                auditSampleSize=auditSampleSize,
                disScore=disScore,
                disTimes=disTimes,
                skip=skip,
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
            disScore = value.safe_get_float_in_key(e, 'DIS Score')
            if disScore != None:
                disScore = int(math.ceil(disScore))
            disTimes = value.safe_get_in_key(e, 'Times')
            skip = value.safe_get_bool_in_key(e, 'Skip')
            item = CheckListItemORT(
                checkListId=checkListId,
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
                disScore=disScore,
                disTimes=disTimes,
                skip=skip,
                )
            batch.append(item)
        if len(batch) > 0:
            CheckListItemORT.objects.bulk_create(batch, batch_size=len(batch))

