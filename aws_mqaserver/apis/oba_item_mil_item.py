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

from aws_mqaserver.models import ObserveType
from aws_mqaserver.models import OBAItemMILItem

import json

logger = logging.getLogger('django')

def _batch_add_mil_items(obaItemId, lob, site, productLine, project, part, type, year, auditorId, auditor, createTime, dicArr):
    batch = []
    for e in dicArr:
        auditDate = value.safe_get_date_in_key(e, 'date')
        severity = value.safe_get_in_key(e, 'severity', '')
        findings = value.safe_get_in_key(e, 'findings', '')
        item = OBAItemMILItem(
            obaItemId=obaItemId,
            lob=lob,
            site=site,
            productLine=productLine,
            project=project,
            part=part,
            type=type,
            year=year,
            vendor=part,
            month=e['month'],
            quarter=e['quarter'],
            auditDate=auditDate,
            severity=severity,
            findings=findings,
            createTime=createTime,
            auditorId=auditorId,
            auditor=auditor,
        )
        batch.append(item)
    if len(batch) > 0:
        OBAItemMILItem.objects.bulk_create(batch, batch_size=len(batch))

