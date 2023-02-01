import sys, os
from django.forms.models import model_to_dict
from django.db.models import Q
from django.db import transaction

from django.core.paginator import Paginator
import logging
from django.conf import settings
import datetime
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

from aws_mqaserver.models import ObserveType
from aws_mqaserver.models import OBAItem
import json

logger = logging.getLogger('django')

@transaction.atomic
def upload_oba_item(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    lob = validator.validate_not_empty(params, 'lob')
    site = validator.validate_not_empty(params, 'site')
    productLine = validator.validate_not_empty(params, 'productLine')
    project = validator.validate_not_empty(params, 'project')
    part = validator.validate_not_empty(params, 'part')
    type = validator.validate_not_empty(params, 'type')
    beginTime = validator.validate_date(params, 'beginTime')
    endTime = validator.validate_date(params, 'endTime')
    year = beginTime.year
    highlight = value.safe_get_in_key(params, 'highlight', '')
    scoreLossItem = validator.validate_not_empty(params, 'scoreLossItem')
    score = validator.validate_float(params, 'score')
    findings = validator.validate_not_empty(params, 'findings')
    auditor = value.safe_get_in_key(params, 'auditor')
    uploadTime = datetime.datetime.now()
    if auditor == None:
        auditor = operator.name

    # audit_type_name = 'OBA'
    # if type == ObserveType.Cosmetic:
    #     audit_type_name = 'OBA Cosmetic'
    # elif type == ObserveType.Surface:
    #     audit_type_name = 'OBA Color'
    # excel_name = lob + '_' + site + '_' + productLine + '_' + project + '_' + part + '_' + audit_type_name + '_' + uploadTime.strftime("%Y%m%d%H%M%S") + '.xlsx'
    # excel_temp_path = tempfile.gettempdir() + '/' + excel_name
    # excel_writer = pandas.ExcelWriter(excel_temp_path)
    # excel_audit_infos = []
    # scoreLossInfo = json.loads(scoreLossItem)
    # findings_items = json.loads(findings)
    # findings_count = len(findings_items)
    # excel_audit_infos = [
    #     ['LOB', lob],
    #     ['Site', site],
    #     ['Product Line', productLine],
    #     ['Project', project],
    #     ['Part', part],
    #     ['Audit Type', audit_type_name],
    #     ['Year', year],
    #     ['Highlight', highlight],
    #     ['Part Quality Score Loss', value.safe_get_in_key(scoreLossInfo, 'partQuality')],
    #     ['Preparation Score Loss', value.safe_get_in_key(scoreLossInfo, 'preparation')],
    #     ['Audit Support Score Loss', value.safe_get_in_key(scoreLossInfo, 'auditSupport')],
    #     ['Critical Issues Score Loss', value.safe_get_in_key(scoreLossInfo, 'criticalIssues')],
    #     ['Score', score],
    #     ['Findings Count', findings_count],
    #     ['Begin Time', beginTime.strftime("%Y-%m-%d %H:%M:%S")],
    #     ['End Time', endTime.strftime("%Y-%m-%d %H:%M:%S")],
    #     ['Audit Remark', auditRemark],
    #     ['Auditor', auditor],
    #     ['Upload Time', uploadTime.strftime("%Y-%m-%d %H:%M:%S")],
    # ]
    # pandas.DataFrame(excel_audit_infos, columns=['Info Key', 'Info Value']).to_excel(excel_writer, sheet_name='Audit Infos', index=False)
    # excel_finds_items = []
    # for item in findings_items:
    #     date = validator.validate_date(item, 'date')
    #     month = date.month
    #     quarter = None
    #     if month < 4:
    #         quarter = 'Q1'
    #     elif month < 7:
    #         quarter = 'Q2'
    #     elif month < 10:
    #         quarter = 'Q3'
    #     else:
    #         quarter = 'Q4'
    #     excel_finds_items.append([
    #         quarter,
    #         date.strftime("%Y-%m-%d"),
    #         value.safe_get_in_key(item, 'severity'),
    #         value.safe_get_in_key(item, 'findings'),
    #     ])
    # pandas.DataFrame(excel_finds_items, columns=['Quarter', 'Audit Date', 'Severity', 'Findings (Descriptions & Baseline)']).to_excel(excel_writer,
    #                                                                                  sheet_name='Audit Findings',
    #                                                                                  index=False)
    # excel_writer.close()
    # box_folder = '/' + team + '/' + lob + '/' + site + '/' + productLine + '/' + project + '/' + part + '/' + audit_type_name
    # excel_stream = open(excel_temp_path, 'rb')
    # box.upload_file(box_folder, excel_name, excel_stream)
    # os.remove(excel_temp_path)

    entry = OBAItem(lob=lob, site=site, productLine=productLine, project=project, part=part, type=type,
                      beginTime=beginTime, endTime=endTime, uploadTime=uploadTime,
                      year=year,
                      highlight=highlight,
                      scoreLossItem=scoreLossItem,
                      score=score,
                      findings=findings,
                      createTime=datetime.datetime.now(),
                      auditorId=operator.id, auditor=auditor)
    entry.save()
    return response.ResponseData({
        'id': entry.id
    })

# Get Check List Items
def get_oba_items_for_year(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    year = validator.validate_integer(params, 'year')
    lob = validator.validate_not_empty(params, 'lob')
    site = validator.validate_not_empty(params, 'site')
    productLine = validator.validate_not_empty(params, 'productLine')
    project = validator.validate_not_empty(params, 'project')
    part = validator.validate_not_empty(params, 'part')
    type = validator.validate_not_empty(params, 'type')
    try:
        list = OBAItem.objects.all().filter(
            year=year,
            lob=lob,
            site=site,
            productLine=productLine,
            project=project,
            part=part,
            type=type).order_by("beginTime")
        if list is None:
            return response.ResponseData([])
        arr = []
        for e in list:
            arr.append(model_to_dict(e))
        return response.ResponseData(arr)
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')