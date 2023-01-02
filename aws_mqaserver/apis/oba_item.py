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

from aws_mqaserver.models import OBAItem
import json

logger = logging.getLogger('django')

@transaction.atomic
def upload_oba_item(request):
    tokenInfo = validator.check_token_info(request)
    operatorName = tokenInfo.get('name')
    operatorId = tokenInfo.get('id')
    params = json.loads(request.body.decode())
    lob = validator.validate_not_empty(params, 'lob')
    site = validator.validate_not_empty(params, 'site')
    productLine = validator.validate_not_empty(params, 'productLine')
    project = validator.validate_not_empty(params, 'project')
    part = validator.validate_not_empty(params, 'part')
    type = validator.validate_integer(params, 'type')
    beginTime = validator.validate_date(params, 'beginTime')
    endTime = validator.validate_date(params, 'endTime')
    year = beginTime.year
    highlight = value.safe_get_key(params, 'highlight')
    scoreLossItem = validator.validate_not_empty(params, 'scoreLossItem')
    score = validator.validate_float(params, 'score')
    findings = validator.validate_not_empty(params, 'findings')
    auditor = value.safe_get_key(params, 'auditor')
    if auditor == None:
        auditor = operatorName
    entry = OBAItem(lob=lob, site=site, productLine=productLine, project=project, part=part, type=type,
                      beginTime=beginTime, endTime=endTime,
                      year=year,
                      highlight=highlight,
                      scoreLossItem=scoreLossItem,
                      score=score,
                      findings=findings,
                      createTime=datetime.datetime.now(),
                      auditorId=operatorId, auditor=auditor)
    entry.save()
    return response.ResponseData({
        'id': entry.id
    })