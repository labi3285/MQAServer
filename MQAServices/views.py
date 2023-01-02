import os

from django.http.response import HttpResponse
from django.http import StreamingHttpResponse
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django import forms

from wsgiref.util import FileWrapper

from MQAServices.models import *

global levelListPath #层级列表地址
global rootFolderPath #根目录地址
global checkListPath #根据产线名拼接的checklist地址
global lineFolderPath #当前产线根目录
global visitHistoryPath #历史visit文件夹地址
global productLineDict #五级产线字典

levelListPath = '/Users/mqa_server/ServerDataBase/ProductLineList/siteLevelData.json'
fileName = 'siteLevelData.json'


# 获取产线层级列表
def downloadLevelContent(request):
    wrapper = FileWrapper(open(levelListPath, 'rb'))
    if request.method == 'GET':
        response = StreamingHttpResponse(wrapper)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(fileName)
        return response
    else:
        return HttpResponse('error')


rootFolderPath = '/Users/mqa_server/ServerDataBase/Acoustic/'


def file_name(file_dir):
    L=[]
    for root,dirs,files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1]=='.json':
                L.append(os.path.join(root,file))
    return (L)


# 下载checklist
def downloadCheckList(request):
    lob = request.POST.get('lob')
    site = request.POST.get('site')
    productLine = request.POST.get('productLine')
    project = request.POST.get('project')
    part = request.POST.get('part')
    checkListPath = rootFolderPath + lob + site + productLine + project + part + '/Checklist/'
    lineFolderPath = rootFolderPath + lob + site + productLine + project + part

    check_empty = file_name(checkListPath)
    if len(check_empty)==0:
        error = 'CheckList not exists'
        print(checkListPath)
        return HttpResponse(error)
    else:
        if request.method == 'POST':
            checklistName = lob + '_' + site + '_' + productLine + '_' + project + '_' + part + '.json'
            checkListFilePath = checkListPath + checklistName
            wrapper = FileWrapper(open(checkListFilePath, 'rb'))
            response = StreamingHttpResponse(wrapper)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{}"'.format(checkListPath)
            return response


# 获取历史visit
def donwnloadVisitHistory(request):
    visitHistoryPath = lineFolderPath + '/History/'
    if not os.listdir(visitHistoryPath):
        return HttpResponse('CheckList not exists')
    else:
        if request.method == 'GET':
            wrapper = FileWrapper(open(visitHistoryPath, 'rb'))
            response = StreamingHttpResponse(wrapper)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{}"'.format(checkListPath)
            return response


class UserForm(forms.Form):
    filename = forms.FileField()


# 上传visit
def uploadVisit(request):
    if request.method == "POST":
        userfrom = UserForm(request.POST, request.FILES)
        if userfrom.is_valid():
            filename  = userfrom.cleaned_data['filename']
            f = Upload()
            f.fullpath = 'AcousticAACiPadX1751Woofer-Tweeter/' + 'History/'
            f.file_path =  filename
            f.save()
            return JsonResponse({"result": 200, "msg": "请求成功, 上传文件"})

        return JsonResponse({"result": 201, "msg": "请求失败"})
    else:
        return JsonResponse({"result": 202, "msg": "请求失败，请求方式错误"})


class FileFieldForm(forms.Form):
    filetype = forms.CharField()
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    # filename = forms.FileField()

def upload_image_video(request):
    if request.method == 'POST':
        fileForm = FileFieldForm(request.POST, request.FILES)
        # userfrom = FileFieldForm(request.POST, request.FILES)
        print(fileForm.is_valid())
        if fileForm.is_valid():
            filetype = fileForm.cleaned_data['filetype']
            print(filetype)
            files = request.FILES.getlist('file_field')
            print(files)
        #     filename = ''
        #     for f in files:
        #         print(f)
        #     file = uploadImgandVideo()
            # file.fullpath = 'AcousticAACiPadX1751Woofer-Tweeter/' + 'History/'
            # file.file_path = filename
            # file.save()
            return JsonResponse({"result": 200, "msg": "请求成功, 上传文件"})

        return JsonResponse({"result": 201, "msg": "请求失败"})
    else:
        return JsonResponse({"result": 202, "msg": "请求失败，请求方式错误"})

def uploadRecordExcel(request):
    if request.method == "POST":
        userfrom = UserForm(request.POST, request.FILES)
        if userfrom.is_valid():
            filename = userfrom.cleaned_data['filename']
            print(filename)
            f = UploadRecord()
            f.savepath = '/Users/mqa_server/ServerDataBase/Acoustic/AcousticAACiPadX1751Woofer-Tweeter/' + 'History/Record/'
            f.fullpath = 'AcousticAACiPadX1751Woofer-Tweeter/' + 'History/Record/'
            f.file_path = filename
            f.save()
            return JsonResponse({"result": 200, "msg": "请求成功, 上传record"})

        return JsonResponse({"result": 201, "msg": "请求失败"})
    else:
        return JsonResponse({"result": 202, "msg": "请求失败，请求方式错误"})


def uploadMILExcel(request):
    if request.method == "POST":
        userfrom = UserForm(request.POST, request.FILES)
        if userfrom.is_valid():
            filename = userfrom.cleaned_data['filename']
            f = UploadMIL()
            f.fullpath = 'AcousticAACiPadX1751Woofer-Tweeter/' + 'History/MIL/'
            f.file_path = filename
            f.save()
            return JsonResponse({"result": 200, "msg": "请求成功, 上传MIL"})

        return JsonResponse({"result": 201, "msg": "请求失败"})
    else:
        return JsonResponse({"result": 202, "msg": "请求失败，请求方式错误"})


# TODO: 1、导出excel文件到对应文件夹
#       2、整理返回体结构
#       3、导出图片、视频，存入数据库
#       4、登录、注册
#       5、图片视频上传需要判断文件类型，且需要适配多个文件同时上传




def jsonFileAddProductline(request):
    return ''

# def registerUser(request):
#


# def login(request):
#