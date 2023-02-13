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

from aws_mqaserver.team_Accessory.models import AccessoryCheckType
from aws_mqaserver.team_Accessory.models import AccessoryAuditItem

from aws_mqaserver.team_Accessory.apis import audit_item_check_item

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
    crossDays = value.safe_get_in_key(params, 'crossDays')
    auditRemark = value.safe_get_in_key(params, 'auditRemark')
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
    audit_items = []
    audit_items_points = []
    if rawJson != None and rawJson != '':
        audit_items = json.loads(rawJson)
        for e in audit_items:
            totalCount += 1
            isDone = value.safe_get_in_key(e, 'isDone', False)
            points = value.safe_get_in_key(e, 'points', [])
            for p in points:
                p['checkItem'] = e['checkItem']
                audit_items_points.append(p)
            if isDone:
                doneCount += 1
            if type == AccessoryCheckType.Glue or type == AccessoryCheckType.Destructive:
                if value.safe_get_in_key(e, 'failCount', 0) > 0:
                    failCount += 1
                else:
                    if isDone:
                        passCount += 1

    # audit_type_name = ''
    # if type == AccessoryCheckType.Glue:
    #     audit_type_name = 'Glue'
    # elif type == AccessoryCheckType.Destructive:
    #     audit_type_name = 'Destructive'
    # excel_name = lob + '_' + site + '_' + productLine + '_' + project + '_' + part + '_' + audit_type_name + '_' + uploadTime.strftime("%Y%m%d%H%M%S") + '.xlsx'
    # excel_temp_path = tempfile.gettempdir() + '/' + excel_name
    # excel_writer = pandas.ExcelWriter(excel_temp_path)
    # excel_audit_infos = []
    # progress = '0.0%%'
    # if totalCount > 0:
    #     p = float(doneCount) / float(totalCount) * 100.0
    #     progress = '%.2f%%' % p
    # if type == AccessoryCheckType.Glue or type == AccessoryCheckType.Destructive:
    #     cross_day_str = None
    #     if crossDays != None:
    #         if crossDays == 1:
    #             cross_day_str = 'TRUE'
    #         else:
    #             cross_day_str = 'FALSE'
    #     excel_audit_infos = [
    #         ['LOB', lob],
    #         ['Site', site],
    #         ['Product Line', productLine],
    #         ['Project', project],
    #         ['Part', part],
    #         ['Audit Type', audit_type_name],
    #         ['Pass Count', passCount],
    #         ['Fail Count', failCount],
    #         ['Done Count', doneCount],
    #         ['Total Count', totalCount],
    #         ['Audit Progress', progress],
    #         ['Begin Time', beginTime.strftime("%Y-%m-%d %H:%M:%S")],
    #         ['End Time', endTime.strftime("%Y-%m-%d %H:%M:%S")],
    #         ['Upload Time', uploadTime.strftime("%Y-%m-%d %H:%M:%S")],
    #         ['Cross Days', cross_day_str],
    #         ['Audit Remark', auditRemark],
    #         ['Auditor', auditor],
    #     ]
    # pandas.DataFrame(excel_audit_infos, columns=['Info Key', 'Info Value']).to_excel(excel_writer, sheet_name='Audit Infos', index=False)
    # excel_audit_items = []
    # if type == AccessoryCheckType.Glue or type == AccessoryCheckType.Destructive:
    #     excel_point_items = []
    #     for item in audit_items:
    #         check_item = item['checkItem']
    #         points = value.safe_get_in_key(item, 'points')
    #         sn = value.safe_get_in_key(check_item, 'sn')
    #         if points != None:
    #             arr = []
    #             if type == AccessoryCheckType.Glue:
    #                 for p in points:
    #                     result = value.safe_get_in_key(p, 'result', 0)
    #                     excel_point_items.append([ sn, result ])
    #             elif type == AccessoryCheckType.Destructive:
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
    #     if type == AccessoryCheckType.Glue:
    #         pandas.DataFrame(excel_point_items, columns=[
    #             'SN', 'Before', 'After', 'Result',
    #         ]).to_excel(excel_writer, sheet_name='Audit Points', index=False)
    #     elif type == AccessoryCheckType.Destructive:
    #         pandas.DataFrame(excel_point_items, columns=[
    #             'SN', 'Result',
    #         ]).to_excel(excel_writer, sheet_name='Audit Points', index=False)
    # excel_writer.close()
    # box_folder = '/Smart_Audit_Database_' + team + '/' + lob + '/' + site + '/' + productLine + '/' + project + '/' + part + '/' + audit_type_name
    # excel_stream = open(excel_temp_path, 'rb')
    # box.upload_file(box_folder, excel_name, excel_stream)
    # os.remove(excel_temp_path)

    entry = AccessoryAuditItem(lob=lob, site=site, productLine=productLine, project=project, part=part, type=type,
                        beginTime=beginTime, endTime=endTime, crossDays=crossDays, auditRemark=auditRemark, uploadTime=uploadTime, passCount=passCount, failCount=failCount, doneCount=doneCount, totalCount=totalCount, rawJson=rawJson, createTime=datetime.datetime.now(),
                          auditorId=operator.id, auditor=auditor)
    entry.save()
    if audit_items != None and len(audit_items) > 0:
        audit_item_check_item._batch_add_check_items(entry.id, lob, site, productLine, project, part, type, operator.id, auditor, uploadTime, audit_items)
    if audit_items_points != None and len(audit_items_points) > 0:
        audit_item_check_item._batch_add_check_items_points(entry.id, lob, site, productLine, project, part, type, operator.id, auditor, uploadTime, audit_items_points)
    return response.ResponseData({
        'id': entry.id
    })
