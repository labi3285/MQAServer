
from django.forms.models import model_to_dict
from django.db.models import Q

from django.core.paginator import Paginator
import logging
from django.conf import settings
import datetime
import traceback

from aws_mqaserver.utils import value
from aws_mqaserver.utils import validator
from aws_mqaserver.utils import response
from aws_mqaserver.utils import token

from aws_mqaserver.models import Line

import json

logger = logging.getLogger('django')

# Add Line
def add_line(request):
    tokenInfo = validator.check_token_info(request)
    operatorLob = tokenInfo.get('lob')
    operatorRole = tokenInfo.get('role')
    params = json.loads(request.body.decode())
    auditType = validator.validate_integer(params, 'auditType')
    lob = validator.validate_not_empty(params, 'lob')
    site = value.safe_get_key(params, 'site')
    productLine = value.safe_get_key(params, 'productLine')
    project = value.safe_get_key(params, 'project')
    part = value.safe_get_key(params, 'part')
    if part != None and project == None:
        return response.ResponseError('Params Error')
    if project != None and productLine == None:
        return response.ResponseError('Params Error')
    if productLine != None and site == None:
        return response.ResponseError('Params Error')  
     
    if operatorRole != 'admin':
        # only admin can add top level
        if site == None:
            return response.ResponseError('Operation Forbidden')
        # only lob_manager and admin can add line
        if operatorRole != 'lob_manager':
            return response.ResponseError('Operation Forbidden') 
        # lob_manager can only add lob sub line
        if lob != operatorLob:
            return response.ResponseError('Operation Forbidden') 
        
    # check duplicate name
    try:
        Line.objects.get(lob=lob, site=site, productLine=productLine, project=project, part=part, auditType=auditType)
        return response.ResponseError('Name Duplicate')
    except Line.DoesNotExist:
        pass
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')
    # add line
    try:
        line = Line(lob=lob, site=site, productLine=productLine, project=project, part=part, auditType=auditType)
        line.save()
        return response.ResponseData('Add Success')
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')

# Delete Line
def delete_line(request):
    tokenInfo = validator.check_token_info(request)
    operatorLob = tokenInfo.get('lob')
    operatorRole = tokenInfo.get('role')
    params = json.loads(request.body.decode())
    id = validator.validate_not_empty(params, 'id')
    line = None
    try:
        line = Line.objects.get(id=id)
    except Line.DoesNotExist:
        return response.ResponseError('Line Not Exist')
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')
    if operatorRole != 'admin':
        # only admin can add top level
        if line.site == None:
            return response.ResponseError('Operation Forbidden')
        # only lob_manager and admin can delete line
        if operatorRole != 'lob_manager':
            return response.ResponseError('Operation Forbidden') 
        # lob_manager can only delete lob sub line
        if line.lob != operatorLob:
            return response.ResponseError('Operation Forbidden') 
    # delete line
    try:
        if line.part != None:
            line.delete()
        else:
            list = None
            if line.project != None:
                list = Line.objects.filter(lob=line.lob, site=line.site, productLine=line.productLine, project=line.project)
            elif line.productLine != None:
                list = Line.objects.filter(lob=line.lob, site=line.site, productLine=line.productLine)
            elif line.site != None:
                list = Line.objects.filter(lob=line.lob, site=line.site)
            elif line.lob != None:
                list = Line.objects.filter(lob=line.lob)
            for e in list:
                e.delete()
        return response.ResponseData('Deleted')        
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')

# Get Lines Page
def get_lines_page(request):
    tokenInfo = validator.check_token_info(request)
    operatorRole = tokenInfo.get('role')
    if operatorRole != 'admin' and operatorRole != 'lob_manager':
        return response.ResponseError('Operation Forbidden')
    params = json.loads(request.body.decode())
    pageNum = validator.validate_not_empty(params, 'pageNum')
    pageSize = validator.validate_not_empty(params, 'pageSize')
    lob = value.safe_get_key(params, 'lob')
    site = value.safe_get_key(params, 'site')
    productLine = value.safe_get_key(params, 'productLine')
    project = value.safe_get_key(params, 'project')
    if project != None:
        if productLine == None:
            return response.ResponseError('Params Error')
    if productLine != None:
        if site == None:
            return response.ResponseError('Params Error')
    if site != None:
        if lob == None:
            return response.ResponseError('Params Error') 
    try:
        list = Line.objects.all()
        if lob != None:
            list = list.filter(lob=lob)
        if site != None:
            list = list.filter(site=site)
        if productLine != None:
            list = list.filter(productLine=productLine)
        if project != None:
            list = list.filter(project=project)
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
    
    
# Get Level Lines
def get_level_lines(request):
    tokenInfo = validator.check_token_info(request)
    params = json.loads(request.body.decode())
    lob = value.safe_get_key(params, 'lob')
    site = value.safe_get_key(params, 'site')
    productLine = value.safe_get_key(params, 'productLine')
    project = value.safe_get_key(params, 'project')
    if project != None:
        if productLine == None or site == None or lob == None:
            return response.ResponseError('Params Error')
    if productLine != None:
        if site == None or lob == None:
            return response.ResponseError('Params Error')
    if site != None:
        if lob == None:
            return response.ResponseError('Params Error')    
    try:
        list = None
        if lob == None:
            list = Line.objects.filter(lob__isnull=False, site__isnull=True)
        else:
            list = Line.objects.filter(lob=lob)
            if site == None:
                list = list.filter(site__isnull=False, productLine__isnull=True)
            else:
                list = list.filter(site=site)
                if productLine == None:
                    list = list.filter(productLine__isnull=False, project__isnull=True)
                else:
                    list = list.filter(productLine=productLine)
                    if project == None:
                        list = list.filter(project__isnull=False, part__isnull=True)
                    else:
                        list = list.filter(project=project).filter(part__isnull=False)
        arr = []
        for e in list:
            arr.append(model_to_dict(e))
        return response.ResponseData(arr)
    except Line.DoesNotExist:
        return response.ResponseData([])
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')


# Get Lines Tree
def get_lines_tree(request):
    # tokenInfo = validator.check_token_info(request)
    try:
        list = Line.objects.all()
        arr = []
        for e in list:
            arr.append(model_to_dict(e))
        lobs_dic = {}
        # filte lob
        for a in arr:
            lob = a.get('lob')
            sub = value.safe_get_key(lobs_dic, lob)
            if sub == None:
                sub = [a]
                lobs_dic[lob] = sub
            else:
                sub.append(a)
        # filte site
        for lob in lobs_dic:
            sites_dic = {}
            for a in lobs_dic.get(lob):
                site = a.get('site')
                sub = value.safe_get_key(sites_dic, site)
                if site == None:
                    pass
                else:
                    if sub == None:
                        sub = [a]
                        sites_dic[site] = sub
                    else:
                        sub.append(a)
            lobs_dic[lob] = sites_dic

        # filte productLine
        for lob in lobs_dic:
            for site in lobs_dic.get(lob):
                productLines_dic = {}
                for a in lobs_dic.get(lob).get(site):
                    productLine = a.get('productLine')
                    sub = value.safe_get_key(productLines_dic, productLine)
                    if productLine == None:
                        pass
                    else:
                        if sub == None:
                            sub = [a]
                            productLines_dic[productLine] = sub
                        else:
                            sub.append(a)
                lobs_dic.get(lob)[site] = productLines_dic

        # filte project
        for lob in lobs_dic:
            for site in lobs_dic.get(lob):
                for productLine in lobs_dic.get(lob).get(site):
                    projects_dic = {}
                    for a in lobs_dic.get(lob).get(site).get(productLine):
                        project = a.get('project')
                        sub = value.safe_get_key(projects_dic, project)
                        if project == None:
                            pass
                        else:
                            if sub == None:
                                sub = [a]
                                projects_dic[project] = sub
                            else:
                                sub.append(a)
                    lobs_dic.get(lob).get(site)[productLine] = projects_dic

        # filte part
        for lob in lobs_dic:
            for site in lobs_dic.get(lob):
                for productLine in lobs_dic.get(lob).get(site):
                    for project in lobs_dic.get(lob).get(site).get(productLine):
                        arr = []
                        for a in lobs_dic.get(lob).get(site).get(productLine).get(project):
                            part = a.get('part')
                            if part != None:
                                arr.append(a)
                        lobs_dic.get(lob).get(site).get(productLine)[project] = arr

        lobs = []
        for lob in lobs_dic:
            sites = []
            for site in lobs_dic.get(lob):
                productLines = []
                for productLine in lobs_dic.get(lob).get(site):
                    projects = []
                    for project in lobs_dic.get(lob).get(site).get(productLine):
                        parts = []
                        for e in lobs_dic.get(lob).get(site).get(productLine).get(project):
                            # e['type'] = 'part'
                            parts.append({
                                'name': e.get('part'),
                                'auditType': e.get('auditType'),
                                'type': 'part'
                            })
                        projects.append({
                            'name': project,
                            'type': 'project',
                            'sub': parts
                        })
                    productLines.append({
                        'name': productLine,
                        'type': 'productLine',
                        'sub': projects
                    })
                sites.append({
                    'name': site,
                    'type': 'site',
                    'sub': productLines
                })
            lobs.append({
                'name': lob,
                'type': 'lob',
                'sub': sites
            })
        return response.ResponseData(lobs)
    except Line.DoesNotExist:
        return response.ResponseData([])
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')