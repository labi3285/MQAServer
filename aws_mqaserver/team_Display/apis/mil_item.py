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

from aws_mqaserver.team_Display.models import DisplayMILItem

import json

logger = logging.getLogger('django')

def update_mil_item(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    id = value.safe_get_in_key(params, 'id')
    type = validator.validate_not_empty(params, 'type')
    lob = validator.validate_not_empty(params, 'lob')
    site = value.safe_get_in_key(params, 'site')
    productLine = value.safe_get_in_key(params, 'productLine')
    project = value.safe_get_in_key(params, 'project')
    part = value.safe_get_in_key(params, 'part')
    if operator.role == 'admin' and operator.team != 'Display':
        return response.ResponseError('Operation Forbidden')
    if (operator.role == 'lob_dri' or operator.role == 'lob_auditor') and (operator.team != 'Display' or not ids.contains_id(lob, operator.lob)):
        return response.ResponseError('Operation Forbidden')
    sn = 0
    createTime = datetime.datetime.now()
    year = createTime.year
    month = createTime.month
    week = int(createTime.strftime("%W")) + 1
    day = createTime.day
    quarter = None
    if month < 4:
        quarter = 1
    elif month < 7:
        quarter = 2
    elif month < 10:
        quarter = 3
    else:
        quarter = 4
    findings = validator.validate_not_empty(params, 'findings')
    processCategory = value.safe_get_in_key(params, 'processCategory')
    keywords = value.safe_get_in_key(params, 'keywords')
    status = value.safe_get_in_key(params, 'status')
    severity = value.safe_get_in_key(params, 'severity')
    line = value.safe_get_in_key(params, 'line')
    station = value.safe_get_in_key(params, 'station')
    issueCategory = value.safe_get_in_key(params, 'issueCategory')
    subCategory = value.safe_get_in_key(params, 'subCategory')
    issueBrief = value.safe_get_in_key(params, 'issueBrief')
    containmentAction = value.safe_get_in_key(params, 'containmentAction')
    correctiveAction = value.safe_get_in_key(params, 'correctiveAction')
    department = value.safe_get_in_key(params, 'department')
    vendorDRI = value.safe_get_in_key(params, 'vendorDRI')
    productCategory = value.safe_get_in_key(params, 'productCategory')
    byAuditCategory = value.safe_get_in_key(params, 'byAuditCategory')
    failureAnalysisRootCause = value.safe_get_in_key(params, 'failureAnalysisRootCause')
    programRelated = value.safe_get_in_key(params, 'programRelated')
    FA = value.safe_get_in_key(params, 'FA')
    CA = value.safe_get_in_key(params, 'CA')
    MILDescription = value.safe_get_in_key(params, 'MILDescription')
    if id == None:
        entry = DisplayMILItem(
            lob=lob,
            site=site,
            productLine=productLine,
            project=project,
            part=part,
            sn=sn,
            type=type,
            year=year,
            month=month,
            day=day,
            quarter=quarter,
            week=week,
            factory=site,
            processCategory=processCategory,
            findings=findings,
            keywords=keywords,
            status=status,
            severity=severity,
            line=line,
            vendor=site,
            station=station,
            projectPart=project + part,
            productCategory=productCategory,
            byAuditCategory=byAuditCategory,
            failureAnalysisRootCause=failureAnalysisRootCause,
            programRelated=programRelated,
            issueCategory=issueCategory,
            subCategory=subCategory,
            issueBrief=issueBrief,
            containmentAction=containmentAction,
            correctiveAction=correctiveAction,
            department=department,
            vendorDRI=vendorDRI,
            FA=FA,
            CA=CA,
            MILDescription=MILDescription,
            createTime=createTime,
            auditorId=operator.id,
            auditor=operator.name,
        )
        entry.save()
        return response.ResponseData('Add Success')
    else:
        entry = DisplayMILItem.objects.get(id=id)
        # entry.lob = lob
        # entry.site = site
        # entry.productLine = productLine
        # entry.project = project
        # entry.part = part
        # entry.sn = sn
        # entry.type = type
        # entry.year = year
        # entry.month = month
        # entry.day = day
        # entry.quarter = quarter
        # entry.week = week
        # entry.factory = site
        # entry.line = line
        # entry.site = site
        # entry.station = station
        # entry.projectPart = project + part
        entry.findings = findings
        entry.processCategory = processCategory
        entry.keywords = keywords
        entry.status = status
        entry.severity = severity
        entry.byAuditCategory = byAuditCategory
        entry.programRelated = programRelated
        entry.issueCategory = issueCategory
        entry.subCategory = subCategory
        entry.issueBrief = issueBrief
        entry.containmentAction = containmentAction
        entry.correctiveAction = correctiveAction
        entry.productCategory = productCategory
        entry.byAuditCategory = byAuditCategory
        entry.failureAnalysisRootCause = failureAnalysisRootCause
        entry.department = department
        entry.vendorDRI = vendorDRI
        entry.FA=FA
        entry.CA = CA
        entry.MILDescription=MILDescription
        entry.updateTime = datetime.datetime.now()
        entry.save()
        return response.ResponseData('Update Success')

# Get MIL Items Page
def get_mil_items_page(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    pageNum = validator.validate_not_empty(params, 'pageNum')
    pageSize = validator.validate_not_empty(params, 'pageSize')
    lob = value.safe_get_in_key(params, 'lob')
    site = value.safe_get_in_key(params, 'site')
    productLine = value.safe_get_in_key(params, 'productLine')
    project = value.safe_get_in_key(params, 'project')
    part = value.safe_get_in_key(params, 'part')
    type = value.safe_get_in_key(params, 'type')
    if operator.role != 'super_admin' and operator.role != 'admin':
        if lob != None and not ids.contains_id(lob, operator.lob):
            return response.ResponseError('Operation Forbidden')
    if part != None:
        if project == None:
            return response.ResponseError('Params Error')
    if project != None:
        if productLine == None:
            return response.ResponseError('Params Error')
    if productLine != None:
        if site == None or lob == None:
            return response.ResponseError('Params Error')
    if site != None:
        if lob == None:
            return response.ResponseError('Params Error') 
    try:
        list = DisplayMILItem.objects.all()
        if type != None:
            list = list.filter(type=type)
        if lob != None:
            list = list.filter(lob=lob)
        if site != None:
            list = list.filter(site=site)
        if productLine != None:
            list = list.filter(productLine=productLine)
        if project != None:
            list = list.filter(project=project)
        if part != None:
            list = list.filter(part=part)
        list = list.order_by('-createTime')
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
    
    
# Delete MIL Item
def delete_mil_item(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    id = validator.validate_not_empty(params, 'id')
    entry = None
    try:
        entry = DisplayMILItem.objects.get(id=id)
    except DisplayMILItem.DoesNotExist:
        return response.ResponseError('MIL Item Not Exist')
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')
    if operator.role != 'super_admin' and operator.role != 'admin':
        # lob_dri can only delete check list in his lob
        if not ids.contains_id(entry.lob, operator.lob):
            return response.ResponseError('Operation Forbidden')
    # delete
    try:
        entry.delete()
        return response.ResponseData('Deleted')        
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')

def _batch_add_mil_items(auditItemId, lob, site, productLine, project, part, type, auditorId, auditor, dicArr):
    batch = []
    for e in dicArr:
        sn = validator.validate_integer(e, 'sn')
        type = value.safe_get_in_key(e, 'processType', type)
        createTime = validator.validate_date(e, 'createTime')
        year = createTime.year
        month = createTime.month
        week = int(createTime.strftime("%W")) + 1
        day = createTime.day
        quarter = None
        if month < 4:
            quarter = 1
        elif month < 7:
            quarter = 2
        elif month < 10:
            quarter = 3
        else:
            quarter = 4
        findings = validator.validate_not_empty(e, 'findings')
        processCategory = value.safe_get_in_key(e, 'processCategory')
        keywords = value.safe_get_in_key(e, 'keywords')
        status = value.safe_get_in_key(e, 'status')
        severity = value.safe_get_in_key(e, 'severity')
        line = value.safe_get_in_key(e, 'line')
        station = value.safe_get_in_key(e, 'station')
        issueCategory = value.safe_get_in_key(e, 'issueCategory')
        subCategory = value.safe_get_in_key(e, 'subCategory')
        issueBrief = value.safe_get_in_key(e, 'issueBrief')
        containmentAction = value.safe_get_in_key(e, 'containmentAction')
        correctiveAction = value.safe_get_in_key(e, 'correctiveAction')
        department = value.safe_get_in_key(e, 'department')
        vendorDRI = value.safe_get_in_key(e, 'vendorDRI')
        byAuditCategory = value.safe_get_in_key(e, 'byAuditCategory')
        programRelated = value.safe_get_in_key(e, 'programRelated')
        item = DisplayMILItem(
            auditItemId=auditItemId,
            lob=lob,
            site=site,
            productLine=productLine,
            project=project,
            part=part,
            sn=sn,
            type=type,
            year=year,
            month=month,
            day=day,
            quarter=quarter,
            week=week,
            factory=site,
            processCategory=processCategory,
            findings=findings,
            keywords=keywords,
            status=status,
            severity=severity,
            line=line,
            vendor=site,
            station=station,
            projectPart=project + part,
            byAuditCategory=byAuditCategory,
            programRelated=programRelated,
            issueCategory=issueCategory,
            subCategory=subCategory,
            issueBrief=issueBrief,
            containmentAction=containmentAction,
            correctiveAction=correctiveAction,
            department=department,
            vendorDRI=vendorDRI,
            createTime=createTime,
            auditorId=auditorId,
            auditor=auditor,
        )
        batch.append(item)
    if len(batch) > 0:
        DisplayMILItem.objects.bulk_create(batch, batch_size=len(batch))

