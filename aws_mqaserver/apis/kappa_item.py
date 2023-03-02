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
from aws_mqaserver.models import KAPPAItem

from aws_mqaserver.apis import kappa_item_score_loss_item
from aws_mqaserver.apis import kappa_item_kappa_skill_score_item

import json

logger = logging.getLogger('django')

@transaction.atomic
def upload_kappa_item(request):
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
    kappaSkillMatrixScores = validator.validate_not_empty(params, 'kappaSkillMatrixScores')
    kappaSkillMatrixAverageScore = validator.validate_float(params, 'kappaSkillMatrixAverageScore')
    auditor = value.safe_get_in_key(params, 'auditor')
    createTime = datetime.datetime.now()
    if auditor == None:
        auditor = operator.name
    scoreLossInfo = json.loads(scoreLossItem)
    kappa_item_kappa_skill_score_items = json.loads(kappaSkillMatrixScores)

    # audit_type_name = 'KAPPA'
    # if type == ObserveType.Cosmetic:
    #     audit_type_name = 'KAPPA Cosmetic'
    # elif type == ObserveType.Surface:
    #     audit_type_name = 'KAPPA Surface'
    # excel_name = lob + '_' + site + '_' + productLine + '_' + project + '_' + part + '_' + audit_type_name + '_' + uploadTime.strftime("%Y%m%d%H%M%S") + '.xlsx'
    # excel_temp_path = tempfile.gettempdir() + '/' + excel_name
    # excel_writer = pandas.ExcelWriter(excel_temp_path)
    # excel_audit_infos = []
    # scoreLossInfo = json.loads(scoreLossItem)
    # excel_summary = [
    #     [lob, site, beginTime.strftime("%Y/%m/%d"), productLine, project, auditor, score, highlight],
    # ]
    # pandas.DataFrame(excel_summary, columns=['LOB', 'Vendor', 'Audit Year/Month/Date', 'Project', 'Component', 'Auditor', 'Score', 'Highlight']).to_excel(excel_writer, sheet_name='Kappa Summary', index=False)
    # a = value.safe_get_in_key(scoreLossInfo, 'kappaFailureRate', 0)
    # b = value.safe_get_in_key(scoreLossInfo, 'sampleCondition', 0)
    # c = value.safe_get_in_key(scoreLossInfo, 'kappaRecord', 0)
    # d = value.safe_get_in_key(scoreLossInfo, 'auditSupport', 0)
    # excel_score_items = [
    #     [lob, site, beginTime.strftime("%Y/%m/%d"), productLine, project, 'A', 'Breakdown', 'Kappa Failure rate', a, 100 - a],
    #     [lob, site, beginTime.strftime("%Y/%m/%d"), productLine, project, 'A', 'Breakdown', 'Sample Condition', b, 100 - b],
    #     [lob, site, beginTime.strftime("%Y/%m/%d"), productLine, project, 'A', 'Breakdown', 'Kappa Record', c, 100 - c],
    #     [lob, site, beginTime.strftime("%Y/%m/%d"), productLine, project, 'A', 'Breakdown', 'Audit Support', d, 100 - d],
    # ]
    # pandas.DataFrame(excel_score_items, columns=['LOB', 'Vendor', 'Audit Year/Month/Date', 'Project', 'Component', 'Item', 'Consmetic Kappa', 'Details', 'Score loss', 'Score']).to_excel(excel_writer, sheet_name='Kappa Score', index=False)
    # excel_fqc_kappa_skill_matrix_items = []
    # matrix_items = json.loads(kappaSkillMatrixScores)
    # for item in matrix_items:
    #     excel_fqc_kappa_skill_matrix_items.append([
    #         value.safe_get_in_key(item, 'name'),
    #         value.safe_get_in_key(item, 'possition'),
    #         value.safe_get_in_key(item, 'score'),
    #         value.safe_get_in_key(item, 'judgement'),
    #     ])
    # pandas.DataFrame(excel_fqc_kappa_skill_matrix_items, columns=['Name', 'Possition', 'Score', 'Judgement']).to_excel(excel_writer,
    #                                                                                  sheet_name='FQC Kappa Skill Matrix Scores',
    #                                                                                  index=False)
    # excel_writer.close()
    # box_folder = '/' + team + '/' + lob + '/' + site + '/' + productLine + '/' + project + '/' + part + '/' + audit_type_name
    # excel_stream = open(excel_temp_path, 'rb')
    # box.upload_file(box_folder, excel_name, excel_stream)
    # os.remove(excel_temp_path)

    entry = KAPPAItem(lob=lob, site=site, productLine=productLine, project=project, part=part, type=type,
                      beginTime=beginTime, endTime=endTime,
                      year=year,
                      highlight=highlight,
                      scoreLossItem=scoreLossItem,
                      score=score,
                      kappaSkillMatrixScores=kappaSkillMatrixScores,
                      kappaSkillMatrixAverageScore=kappaSkillMatrixAverageScore,
                      createTime=createTime,
                      auditorId=operator.id, auditor=auditor)
    entry.save()
    if type == ObserveType.Cosmetic:
        kappa_item_score_loss_item._batch_add_score_loss_items(entry.id, lob, site, productLine, project, part, type, year, operator.id, auditor, createTime, [
            { 'item': 'A', 'breakDown': 'Kappa Failure Rate', 'scoreLoss': value.safe_get_in_key(scoreLossInfo, 'kappaFailureRate') },
            { 'item': 'B', 'breakDown': 'Sample Condition', 'scoreLoss': value.safe_get_in_key(scoreLossInfo, 'sampleCondition') },
            { 'item': 'C', 'breakDown': 'Kappa Record', 'scoreLoss': value.safe_get_in_key(scoreLossInfo, 'kappaRecord') },
            { 'item': 'D', 'breakDown': 'Audit Support', 'scoreLoss': value.safe_get_in_key(scoreLossInfo, 'auditSupport') },
        ])
    elif type == ObserveType.Surface:
        kappa_item_score_loss_item._batch_add_score_loss_items(entry.id, lob, site, productLine, project, part, type, year, operator.id, auditor, createTime, [
            { 'item': 'A', 'breakDown': 'Method', 'scoreLoss': value.safe_get_in_key(scoreLossInfo, 'method') },
            { 'item': 'B', 'breakDown': 'Equipment Fixture', 'scoreLoss': value.safe_get_in_key(scoreLossInfo, 'equipmentFixture') },
            { 'item': 'C', 'breakDown': 'Audit Support', 'scoreLoss': value.safe_get_in_key(scoreLossInfo, 'auditSupport') },
            { 'item': 'D', 'breakDown': 'Part Quality', 'scoreLoss': value.safe_get_in_key(scoreLossInfo, 'partQuality') },
            { 'item': 'E', 'breakDown': 'Critical Issues', 'scoreLoss': value.safe_get_in_key(scoreLossInfo, 'criticalIssues') },
        ])
    if kappa_item_kappa_skill_score_items != None and len(kappa_item_kappa_skill_score_items) > 0:
        kappa_item_kappa_skill_score_item._batch_add_score_items(entry.id, lob, site, productLine, project, part, type, year, operator.id, auditor, createTime, kappa_item_kappa_skill_score_items)
    return response.ResponseData({
        'id': entry.id
    })


# Get Check List Items
def get_kappa_items_for_year(request):
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
        list = KAPPAItem.objects.all().filter(
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