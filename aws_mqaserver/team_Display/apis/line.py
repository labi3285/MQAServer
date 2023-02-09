import sys, os
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
from aws_mqaserver.utils import ids

from aws_mqaserver.models import User
from aws_mqaserver.team_Display.models import DisplayLine

import json

logger = logging.getLogger('django')

# Add Line
@transaction.atomic
def add_line(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    lob = validator.validate_not_empty(params, 'lob')
    site = value.safe_get_in_key(params, 'site')
    productLine = value.safe_get_in_key(params, 'productLine')
    project = value.safe_get_in_key(params, 'project')
    part = value.safe_get_in_key(params, 'part')
    if part != None and project == None:
        return response.ResponseError('Params Error')
    if project != None and productLine == None:
        return response.ResponseError('Params Error')
    if productLine != None and site == None:
        return response.ResponseError('Params Error')
    if operator.role != 'super_admin' and operator.role != 'admin':
        # only lob_dri and admin can add line
        if operator.role != 'lob_dri':
            return response.ResponseError('Operation Forbidden')
        # lob_dri can only add lob sub line
        if site != None and not ids.contains_id(lob, operator.lob):
            return response.ResponseError('Operation Forbidden')
    # check duplicate name
    try:
        DisplayLine.objects.get(lob=lob, site=site, productLine=productLine, project=project, part=part)
        return response.ResponseError('Name Duplicate')
    except DisplayLine.DoesNotExist:
        pass
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')
    # DRI create lob should add himself to this lob
    if site == None and operator.role == 'lob_dri':
        user = User.objects.get(id=operator.id)
        user.lob = user.lob + lob + '/'
        user.save()
    # add line
    line = DisplayLine(lob=lob, site=site, productLine=productLine, project=project, part=part)
    line.save()
    return response.ResponseData('Add Success')

# Delete Line
def delete_line(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    id = validator.validate_not_empty(params, 'id')
    line = None
    try:
        line = DisplayLine.objects.get(id=id)
    except DisplayLine.DoesNotExist:
        return response.ResponseError('Line Not Exist')
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')
    if operator.role != 'super_admin' and operator.role != 'admin':
        # only admin can delete top level
        if line.site == None:
            return response.ResponseError('Operation Forbidden')
        # only lob_dri and admin can delete line
        if operator.role != 'lob_dri':
            return response.ResponseError('Operation Forbidden') 
        # lob_dri can only delete lob sub line
        if not ids.contains_id(line.lob, operator.lob):
            return response.ResponseError('Operation Forbidden') 
    # delete line
    try:
        if line.part != None:
            line.delete()
        else:
            list = None
            if line.project != None:
                list = DisplayLine.objects.filter(lob=line.lob, site=line.site, productLine=line.productLine, project=line.project)
            elif line.productLine != None:
                list = DisplayLine.objects.filter(lob=line.lob, site=line.site, productLine=line.productLine)
            elif line.site != None:
                list = DisplayLine.objects.filter(lob=line.lob, site=line.site)
            elif line.lob != None:
                list = DisplayLine.objects.filter(lob=line.lob)
            for e in list:
                e.delete()
        return response.ResponseData('Deleted')        
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')

# Get Lines Page
def get_lines_page(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    pageNum = validator.validate_not_empty(params, 'pageNum')
    pageSize = validator.validate_not_empty(params, 'pageSize')
    lob = value.safe_get_in_key(params, 'lob')
    site = value.safe_get_in_key(params, 'site')
    productLine = value.safe_get_in_key(params, 'productLine')
    project = value.safe_get_in_key(params, 'project')
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
        list = DisplayLine.objects.all()
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
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    lob = value.safe_get_in_key(params, 'lob')
    site = value.safe_get_in_key(params, 'site')
    productLine = value.safe_get_in_key(params, 'productLine')
    project = value.safe_get_in_key(params, 'project')
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
            list = DisplayLine.objects.filter(lob__isnull=False, site__isnull=True)
        else:
            list = DisplayLine.objects.filter(lob=lob)
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
    except DisplayLine.DoesNotExist:
        return response.ResponseData([])
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')


# Get Lines Tree
def get_lines_tree(request):
    operator = validator.checkout_token_user(request)
    params = json.loads(request.body.decode())
    try:
        list = DisplayLine.objects.all()
        arr = []
        for e in list:
            arr.append(model_to_dict(e))

        info_cache = {}
        lobs_dic = {}
        # filte lob
        for a in arr:
            lob = a.get('lob')
            sub = value.safe_get_in_key(lobs_dic, lob)
            if sub == None:
                sub = [a]
                lobs_dic[lob] = sub
            else:
                sub.append(a)
            if a.get('site') == None:
                info_cache[lob] = a

        # filte site
        for lob in lobs_dic:
            sites_dic = {}
            for a in lobs_dic.get(lob):
                site = a.get('site')
                sub = value.safe_get_in_key(sites_dic, site)
                if site == None:
                    pass
                else:
                    if sub == None:
                        sub = [a]
                        sites_dic[site] = sub
                    else:
                        sub.append(a)
                    if a.get('productLine') == None:
                        info_cache[lob + '/' + site] = a
            lobs_dic[lob] = sites_dic

        # filte productLine
        for lob in lobs_dic:
            for site in lobs_dic.get(lob):
                productLines_dic = {}
                for a in lobs_dic.get(lob).get(site):
                    productLine = a.get('productLine')
                    sub = value.safe_get_in_key(productLines_dic, productLine)
                    if productLine == None:
                        pass
                    else:
                        if sub == None:
                            sub = [a]
                            productLines_dic[productLine] = sub
                        else:
                            sub.append(a)
                        if a.get('project') == None:
                            info_cache[lob + '/' + site + '/' + productLine] = a
                lobs_dic.get(lob)[site] = productLines_dic

        # filte project
        for lob in lobs_dic:
            for site in lobs_dic.get(lob):
                for productLine in lobs_dic.get(lob).get(site):
                    projects_dic = {}
                    for a in lobs_dic.get(lob).get(site).get(productLine):
                        project = a.get('project')
                        sub = value.safe_get_in_key(projects_dic, project)
                        if project == None:
                            pass
                        else:
                            if sub == None:
                                sub = [a]
                                projects_dic[project] = sub
                            else:
                                sub.append(a)
                            if a.get('part') == None:
                                info_cache[lob + '/' + site + '/' + productLine + '/' + project] = a
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
            sites_check_list_uploaded = 0
            sites_check_list_total = 0
            for site in lobs_dic.get(lob):
                productLines = []
                productLines_check_list_uploaded = 0
                productLines_check_list_total = 0
                for productLine in lobs_dic.get(lob).get(site):
                    projects = []
                    projects_check_list_uploaded = 0
                    projects_check_list_total = 0
                    for project in lobs_dic.get(lob).get(site).get(productLine):
                        parts = []
                        parts_check_list_uploaded = 0
                        parts_check_list_total = 0
                        for e in lobs_dic.get(lob).get(site).get(productLine).get(project):
                            parts_check_list_total += 1
                            checkListId_Enclosure = value.safe_get_in_key(e, 'checkListId_Enclosure')
                            if checkListId_Enclosure != None:
                                parts_check_list_uploaded += 1
                            parts.append({
                                'id': e.get('id'),
                                'lob': lob,
                                'site': site,
                                'productLine': productLine,
                                'project': project,
                                'part': e.get('part'),
                                'name': e.get('part'),
                                'type': 'part',
                                'checkListId_Enclosure': checkListId_Enclosure,
                                'checkListUploaded': parts_check_list_uploaded,
                                'checkListTotal': parts_check_list_total,
                            })
                        project_info = info_cache.get(lob + '/' + site + '/' + productLine + '/' + project)
                        projects.append({
                            'id': project_info.get('id'),
                            'lob': lob,
                            'site': site,
                            'productLine': productLine,
                            'project': project,
                            'name': project,
                            'type': 'project',
                            'sub': parts,
                            'checkListUploaded': parts_check_list_uploaded,
                            'checkListTotal': parts_check_list_total,
                        })
                        projects_check_list_uploaded += parts_check_list_uploaded
                        projects_check_list_total += parts_check_list_total
                    productLine_info = info_cache.get(lob + '/' + site + '/' + productLine)
                    productLines.append({
                        'id': productLine_info.get('id'),
                        'lob': lob,
                        'site': site,
                        'productLine': productLine,
                        'name': productLine,
                        'type': 'productLine',
                        'sub': projects,
                        'checkListUploaded': projects_check_list_uploaded,
                        'checkListTotal': projects_check_list_total,
                    })
                    productLines_check_list_uploaded += projects_check_list_uploaded
                    productLines_check_list_total += projects_check_list_total
                site_info = info_cache.get(lob + '/' + site)
                sites.append({
                    'id': site_info.get('id'),
                    'lob': lob,
                    'site': site,
                    'name': site,
                    'type': 'site',
                    'sub': productLines,
                    'checkListUploaded': productLines_check_list_uploaded,
                    'checkListTotal': productLines_check_list_total,
                })
                sites_check_list_uploaded += productLines_check_list_uploaded
                sites_check_list_total += productLines_check_list_total
            lob_info = info_cache.get(lob)
            lobs.append({
                'id': lob_info.get('id'),
                'lob': lob,
                'name': lob,
                'type': 'lob',
                'sub': sites,
                'checkListUploaded': sites_check_list_uploaded,
                'checkListTotal': sites_check_list_total,
            })
        return response.ResponseData(lobs)
    except DisplayLine.DoesNotExist:
        return response.ResponseData([])
    except Exception:
        traceback.print_exc()
        return response.ResponseError('System Error')