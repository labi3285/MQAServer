from django.forms.models import model_to_dict
from django.db.models import Q
from django.db import transaction

from django.core.paginator import Paginator
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
    year = beginTime.year
    highlight = value.safe_get_in_key(params, 'highlight')
    scoreLossItem = validator.validate_not_empty(params, 'scoreLossItem')
    score = validator.validate_float(params, 'score')
    FQCKappaSkillMatrixScores = validator.validate_not_empty(params, 'FQCKappaSkillMatrixScores')
    FQCKappaSkillMatrixAverageScore = validator.validate_float(params, 'FQCKappaSkillMatrixAverageScore')
    auditor = value.safe_get_in_key(params, 'auditor')
    if auditor == None:
        auditor = operator.name
    entry = KAPPAItem(team=team, lob=lob, site=site, productLine=productLine, project=project, part=part, type=type,
                      beginTime=beginTime, endTime=endTime,
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
    type = validator.validate_integer(params, 'type')
    try:
        list = KAPPAItem.objects.all().filter(year=year, type=type).order_by("beginTime")
        if list is None:
            return response.ResponseData([])
        arr = []
        for e in list:
            arr.append(model_to_dict(e))
        return response.ResponseData(arr)
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')