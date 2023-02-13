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

from aws_mqaserver.models import CheckType
from aws_mqaserver.models import AuditItem
from aws_mqaserver.apis import audit_item_check_item
from aws_mqaserver.apis import mil_item

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
    type = validator.validate_not_empty(params, 'type')
    beginTime = validator.validate_date(params, 'beginTime')
    endTime = validator.validate_date(params, 'endTime')
    rawJsonBase64 = validator.validate_not_empty(params, 'rawJson')
    rawJson = base64.base64ToString(rawJsonBase64)
    auditor = value.safe_get_in_key(params, 'auditor')
    uploadTime = datetime.datetime.now()
    if auditor == None:
        auditor = operator.name
    skipCount = 0
    passCount = 0
    failCount = 0
    doneCount = 0
    totalCount = 0
    findingCount = 0
    all_findings = None
    audit_items = []
    if rawJson != None and rawJson != '':
        audit_items = json.loads(rawJson)
        all_findings = []
        for e in audit_items:
            totalCount += 1
            isDone = value.safe_get_in_key(e, 'isDone', False)
            if isDone:
                doneCount += 1
            if value.safe_get_in_key(e, 'isSkip', False):
                skipCount += 1
            findings = value.safe_get_in_key(e, 'findings')
            if findings != None and len(findings) > 0:
                e['findingsCount'] = len(findings)
                failCount += 1
                for f in findings:
                    findingCount += 1
                    all_findings.append(f)
            else:
                e['findingsCount'] = 0
                if isDone:
                    passCount += 1

    # audit_type_name = ''
    # if type == CheckType.Module:
    #     audit_type_name = 'Module'
    # elif type == CheckType.Enclosure:
    #     audit_type_name = 'Enclosure'
    # elif type == CheckType.ORT:
    #     audit_type_name = 'ORT'
    # elif type == CheckType.Glue:
    #     audit_type_name = 'Glue'
    # elif type == CheckType.Destructive:
    #     audit_type_name = 'Destructive'
    # excel_name = lob + '_' + site + '_' + productLine + '_' + project + '_' + part + '_' + audit_type_name + '_' + uploadTime.strftime("%Y%m%d%H%M%S") + '.xlsx'
    # excel_temp_path = tempfile.gettempdir() + '/' + excel_name
    # excel_writer = pandas.ExcelWriter(excel_temp_path)
    # excel_audit_infos = []
    # progress = '0.0%%'
    # if totalCount > 0:
    #     p = float(doneCount) / float(totalCount) * 100.0
    #     progress = '%.2f%%' % p
    # if type == CheckType.Module or type == CheckType.Enclosure or type == CheckType.ORT:
    #     excel_audit_infos = [
    #         ['LOB', lob],
    #         ['Site', site],
    #         ['Product Line', productLine],
    #         ['Project', project],
    #         ['Part', part],
    #         ['Audit Type', audit_type_name],
    #         ['Skip Count', skipCount],
    #         ['Pass Count', passCount],
    #         ['Fail Count', failCount],
    #         ['Done Count', doneCount],
    #         ['Total Count', totalCount],
    #         ['Finding Count', findingCount],
    #         ['Audit Progress', progress],
    #         ['Begin Time', beginTime.strftime("%Y-%m-%d %H:%M:%S")],
    #         ['End Time', endTime.strftime("%Y-%m-%d %H:%M:%S")],
    #         ['Auditor', auditor],
    #         ['Upload Time', uploadTime.strftime("%Y-%m-%d %H:%M:%S")],
    #     ]
    # pandas.DataFrame(excel_audit_infos, columns=['Info Key', 'Info Value']).to_excel(excel_writer, sheet_name='Audit Infos', index=False)
    # excel_audit_items = []
    # if type == CheckType.Module:
    #     for item in audit_items:
    #         check_item = item['checkItem']
    #         excel_audit_items.append([
    #             value.safe_get_in_key(check_item, 'sn'),
    #             value.safe_get_in_key(check_item, 'mainProcess'),
    #             value.safe_get_in_key(check_item, 'subProcess'),
    #             value.safe_get_in_key(check_item, 'checkItem'),
    #             value.safe_get_in_key(check_item, 'checkResult'),
    #             value.safe_get_in_key(check_item, 'sampleUnit'),
    #             value.safe_get_in_key(check_item, 'sampleSize'),
    #             value.safe_get_in_key(check_item, 'auditSampleSize'),
    #             value.safe_get_in_key(check_item, 'frenquencyBasis'),
    #             value.safe_get_in_key(check_item, 'ifCtq'),
    #             value.safe_get_in_key(check_item, 'measurementEquipment'),
    #             value.safe_get_in_key(check_item, 'LSL'),
    #             value.safe_get_in_key(check_item, 'USL'),
    #             value.safe_get_in_key(check_item, 'LCL'),
    #             value.safe_get_in_key(check_item, 'UCL'),
    #             value.safe_get_in_key(check_item, 'controlType'),
    #             value.safe_get_in_key(check_item, 'controlMethod'),
    #             value.safe_get_in_key(check_item, 'controlCriteria'),
    #             value.safe_get_in_key(check_item, 'responsePlan'),
    #             value.safe_get_in_key(check_item, 'sopNo'),
    #             value.safe_get_in_key(check_item, 'result'),
    #             value.safe_get_in_key(check_item, 'disScore'),
    #             value.safe_get_in_key(check_item, 'disTimes'),
    #             value.safe_get_in_key(check_item, 'skip'),
    #             value.safe_get_in_key(item, 'peopleTrain'),
    #             value.safe_get_in_key(item, 'machineMaintenance'),
    #             value.safe_get_in_key(item, 'onsiteVerify'),
    #             value.safe_get_in_key(item, 'materialHandling'),
    #             value.safe_get_in_key(item, 'environmentSetting'),
    #             value.safe_get_in_key(item, 'workshopLineMachine'),
    #             value.safe_get_in_key(item, 'result'),
    #             value.safe_get_in_key(item, 'findingsCount'),
    #             value.safe_get_in_key(item, 'isSkip'),
    #             value.safe_get_in_key(item, 'isDone'),
    #         ])
    #     pandas.DataFrame(excel_audit_items, columns=[
    #         'SN', 'Main Process', 'Sub Process', 'Check Item',
    #         'Check Result', 'Sample Unit', 'Sample Size', 'Audit Sample Size', 'Frenquency Basis', 'If Ctq', 'Measurement Equipment', 'LSL', 'USL', 'LCL', 'UCL',
    #         'Control Type', 'Control Method', 'Control Criteria', 'Response Plan', 'Sop No.', 'Result', 'DIS Score', 'DIS Times', 'DIS Skip',
    #         'People Train', 'Machine Maintenance', 'Onsite Verify', 'Material Handling', 'Environment Setting', 'Workshop Line Machine', 'Result',
    #         'Findings Count', 'Is Skip', 'Is Done',
    #     ]).to_excel(excel_writer, sheet_name='Audit Detail', index=False)
    # elif type == CheckType.Enclosure:
    #     for item in audit_items:
    #         check_item = item['checkItem']
    #         excel_audit_items.append([
    #             value.safe_get_in_key(check_item, 'sn'),
    #             value.safe_get_in_key(check_item, 'mainProcess'),
    #             value.safe_get_in_key(check_item, 'subProcess'),
    #             value.safe_get_in_key(check_item, 'checkItems'),
    #             value.safe_get_in_key(check_item, 'samplingSize'),
    #             value.safe_get_in_key(check_item, 'disScore'),
    #             value.safe_get_in_key(check_item, 'disTimes'),
    #             value.safe_get_in_key(check_item, 'skip'),
    #             value.safe_get_in_key(item, 'records'),
    #             value.safe_get_in_key(item, 'result'),
    #             value.safe_get_in_key(item, 'findingsCount'),
    #             value.safe_get_in_key(item, 'isSkip'),
    #             value.safe_get_in_key(item, 'isDone'),
    #         ])
    #     pandas.DataFrame(excel_audit_items, columns=[
    #         'SN', 'Main Process', 'Sub Process', 'Check Items', 'Sampling Size', 'DIS Score', 'DIS Times', 'DIS Skip',
    #         'Records', 'Result',
    #         'Findings Count', 'Is Skip', 'Is Done',
    #     ]).to_excel(excel_writer, sheet_name='Audit Detail', index=False)
    # elif type == CheckType.ORT:
    #     for item in audit_items:
    #         check_item = item['checkItem']
    #         excel_audit_items.append([
    #             value.safe_get_in_key(check_item, 'sn'),
    #             value.safe_get_in_key(check_item, 'project'),
    #             value.safe_get_in_key(check_item, 'testItem'),
    #             value.safe_get_in_key(check_item, 'testConditionParameter'),
    #             value.safe_get_in_key(check_item, 'equipment'),
    #             value.safe_get_in_key(check_item, 'fixtureYN'),
    #             value.safe_get_in_key(check_item, 'sampleOrientation'),
    #             value.safe_get_in_key(check_item, 'recoveryTime'),
    #             value.safe_get_in_key(check_item, 'sampleSize'),
    #             value.safe_get_in_key(check_item, 'samplingFreq'),
    #             value.safe_get_in_key(check_item, 'duration'),
    #             value.safe_get_in_key(check_item, 'readPoint'),
    #             value.safe_get_in_key(check_item, 'passFailCriteria'),
    #             value.safe_get_in_key(check_item, 'OCAP'),
    #             value.safe_get_in_key(item, 'result'),
    #             value.safe_get_in_key(item, 'isDone'),
    #         ])
    #     pandas.DataFrame(excel_audit_items, columns=[
    #         'SN', 'Project', 'Test Item', 'Test Condition/Parameter', 'Equipment', 'Fixture (Y/N)', 'Sample Orientation', 'Recovery Time', 'Sample Size', 'Sampling Freq.', 'Duration', 'Read Point', 'Pass/Fail Criteria', 'OCAP',
    #         'Result',
    #         'Is Done',
    #     ]).to_excel(excel_writer, sheet_name='Audit Detail', index=False)
    # elif type == CheckType.Glue or type == CheckType.Destructive:
    #     excel_point_items = []
    #     for item in audit_items:
    #         check_item = item['checkItem']
    #         points = value.safe_get_in_key(item, 'points')
    #         sn = value.safe_get_in_key(check_item, 'sn')
    #         if points != None:
    #             arr = []
    #             if type == CheckType.Glue:
    #                 for p in points:
    #                     result = value.safe_get_in_key(p, 'result', 0)
    #                     excel_point_items.append([ sn, result ])
    #             elif type == CheckType.Destructive:
    #                 for p in points:
    #                     result = value.safe_get_in_key(p, 'result', 0)
    #                     excel_point_items.append([ sn, result ])
    #             fmt_points = ';'.join(arr)
    #         excel_audit_items.append([
    #             sn,
    #             value.safe_get_in_key(check_item, 'theClass'),
    #             value.safe_get_in_key(check_item, 'lineShift'),
    #             value.safe_get_in_key(check_item, 'site'),
    #             value.safe_get_in_key(check_item, 'projects'),
    #             value.safe_get_in_key(check_item, 'item'),
    #             value.safe_get_in_key(check_item, 'unit'),
    #             value.safe_get_in_key(check_item, 'LSL'),
    #             value.safe_get_in_key(check_item, 'USL'),
    #             value.safe_get_in_key(item, 'passCount'),
    #             value.safe_get_in_key(item, 'failCount'),
    #             value.safe_get_in_key(item, 'totalCount'),
    #             value.safe_get_in_key(item, 'isDone'),
    #         ])
    #     pandas.DataFrame(excel_audit_items, columns=[
    #         'SN', 'Class', 'Line&Shift', 'Site', 'Projects', 'Item', 'Unit', 'LSL', 'USL', 'Pass Points Count', 'Fail Points Count', 'Total Points Count', 'Is Done',
    #     ]).to_excel(excel_writer, sheet_name='Audit Detail', index=False)
    #     if type == CheckType.Glue:
    #         pandas.DataFrame(excel_point_items, columns=[
    #             'SN', 'Before', 'After', 'Result',
    #         ]).to_excel(excel_writer, sheet_name='Audit Points', index=False)
    #     elif type == CheckType.Destructive:
    #         pandas.DataFrame(excel_point_items, columns=[
    #             'SN', 'Result',
    #         ]).to_excel(excel_writer, sheet_name='Audit Points', index=False)
    # excel_finding_items = []
    # if all_findings != None:
    #     for item in all_findings:
    #         excel_finding_items.append([
    #             value.safe_get_in_key(item, 'sn'),
    #             value.safe_get_in_key(item, 'findings'),
    #             value.safe_get_in_key(item, 'keywords'),
    #             value.safe_get_in_key(item, 'status'),
    #             value.safe_get_in_key(item, 'severity'),
    #             value.safe_get_in_key(item, 'station'),
    #             value.safe_get_in_key(item, 'line'),
    #             value.safe_get_in_key(item, 'processCategory'),
    #             value.safe_get_in_key(item, 'programRelated'),
    #             value.safe_get_in_key(item, 'failureAnalysisRootCause'),
    #             value.safe_get_in_key(item, 'issueCategory'),
    #             value.safe_get_in_key(item, 'subCategory'),
    #             value.safe_get_in_key(item, 'containmentAction'),
    #             value.safe_get_in_key(item, 'correctiveAction'),
    #             value.safe_get_in_key(item, 'department'),
    #             value.safe_get_in_key(item, 'vendorDRI'),
    #             value.safe_get_in_key(item, 'issueBrief'),
    #         ])
    # if type == CheckType.Module or type == CheckType.Enclosure or type == CheckType.ORT:
    #     pandas.DataFrame(excel_finding_items, columns=[
    #         'SN', 'Findings', 'Keywords', 'Status', 'Severity', 'Station', 'Line',
    #         'Process Category', 'Program Related', 'Failure Analysis Root Cause', 'Issue Category', 'Sub Category',
    #         'Containment Action', 'Corrective Action', 'Department', 'Vendor DRI', 'Issue Brief',
    #     ]).to_excel(excel_writer, sheet_name='Audit Findings', index=False)
    # excel_writer.close()
    # box_folder = '/Smart_Audit_Database_' + team + '/' + lob + '/' + site + '/' + productLine + '/' + project + '/' + part + '/' + audit_type_name
    # excel_stream = open(excel_temp_path, 'rb')
    # box.upload_file(box_folder, excel_name, excel_stream)
    # os.remove(excel_temp_path)

    entry = AuditItem(lob=lob, site=site, productLine=productLine, project=project, part=part, type=type,
                        beginTime=beginTime, endTime=endTime, uploadTime=uploadTime, skipCount=skipCount, passCount=passCount, failCount=failCount, doneCount=doneCount, totalCount=totalCount, findingCount=findingCount, createTime=datetime.datetime.now(),
                          auditorId=operator.id, auditor=auditor)
    entry.save()
    if audit_items != None and len(audit_items) > 0:
        audit_item_check_item._batch_add_check_items(entry.id, lob, site, productLine, project, part, type, operator.id, auditor, uploadTime, audit_items)
    if all_findings != None and len(all_findings) > 0:
        mil_item._batch_add_mil_items(entry.id, lob, site, productLine, project, part, type, operator.id, auditor, all_findings)
        return response.ResponseData({
            'id': entry.id
        })
    else:
        return response.ResponseData({
            'id': entry.id
        })
