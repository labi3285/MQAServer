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
import json

logger = logging.getLogger('django')

@transaction.atomic
def upload_kappa_item(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    team = validator.get_team(params, operator)
    lob = validator.validate_not_empty(params, 'lob')
    site = validator.validate_not_empty(params, 'site')
    productLine = validator.validate_not_empty(params, 'productLine')
    project = validator.validate_not_empty(params, 'project')
    part = validator.validate_not_empty(params, 'part')
    type = validator.validate_integer(params, 'type')
    beginTime = validator.validate_date(params, 'beginTime')
    endTime = validator.validate_date(params, 'endTime')
    crossDays = value.safe_get_in_key(params, 'crossDays')
    auditRemark = value.safe_get_in_key(params, 'auditRemark')
    year = beginTime.year
    highlight = value.safe_get_in_key(params, 'highlight', '')
    scoreLossItem = validator.validate_not_empty(params, 'scoreLossItem')
    score = validator.validate_float(params, 'score')
    FQCKappaSkillMatrixScores = validator.validate_not_empty(params, 'FQCKappaSkillMatrixScores')
    FQCKappaSkillMatrixAverageScore = validator.validate_float(params, 'FQCKappaSkillMatrixAverageScore')
    auditor = value.safe_get_in_key(params, 'auditor')
    uploadTime = datetime.datetime.now()
    if auditor == None:
        auditor = operator.name

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
    # matrix_items = json.loads(FQCKappaSkillMatrixScores)
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

    entry = KAPPAItem(team=team, lob=lob, site=site, productLine=productLine, project=project, part=part, type=type,
                      beginTime=beginTime, endTime=endTime, uploadTime=uploadTime, crossDays=crossDays, auditRemark=auditRemark,
                      year=year,
                      highlight=highlight,
                      scoreLossItem=scoreLossItem,
                      score=score,
                      FQCKappaSkillMatrixScores=FQCKappaSkillMatrixScores,
                      FQCKappaSkillMatrixAverageScore=FQCKappaSkillMatrixAverageScore,
                      createTime=datetime.datetime.now(),
                      auditorId=operator.id, auditor=auditor)
    entry.save()
    return response.ResponseData({
        'id': entry.id
    })


# Get Check List Items
def get_kappa_items_for_year(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    year = validator.validate_integer(params, 'year')
    team = validator.get_team(params, operator)
    lob = validator.validate_not_empty(params, 'lob')
    site = validator.validate_not_empty(params, 'site')
    productLine = validator.validate_not_empty(params, 'productLine')
    project = validator.validate_not_empty(params, 'project')
    part = validator.validate_not_empty(params, 'part')
    type = validator.validate_integer(params, 'type')
    try:
        list = KAPPAItem.objects.all().filter(
            year=year,
            team=team,
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