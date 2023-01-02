from django.db import models
import os
import uuid


class Visit(models.Model):
    visitId = models.AutoField('id', primary_key=True)
    lob = models.CharField('lob', max_length=50)
    site = models.CharField('site', max_length=50)
    productLine = models.CharField('productLine', max_length=50)
    project = models.CharField('project', max_length=50)
    part = models.CharField('part/color', max_length=50)
    createDate = models.DateTimeField('创建时间', auto_now_add=True)
    modifyDate = models.DateTimeField('修改时间', auto_now=True, null=True)
    path = models.CharField('路径', max_length=100, null=False)
    visitJson = models.CharField('visitJson', null=False, max_length=200)
    pic = models.CharField('图片文件夹路径', max_length=150)
    video = models.CharField('视频文件夹路径', max_length=150)
    record = models.CharField('record文件夹路径', max_length=150)
    mil = models.CharField('mil文件夹路径', max_length=150)

    class Meta:
        db_table = 'Visit'


# TODO:完整路径登记不完整
class Upload(models.Model):
    def image_upload_to(instance, filename):
        return '{0}/{filename}'.format(instance.fullpath, filename=filename)

    fullpath = models.CharField('完整路径', max_length=150)
    file_path = models.FileField(upload_to=image_upload_to)
    createDate = models.DateTimeField('创建时间', auto_now_add=True)


class UploadRecord(models.Model):
    def file_upload_to(instance, filename):
        return '{0}/{filename}'.format(instance.fullpath, filename=filename)

    fullpath = models.CharField(max_length=150)
    savepath = models.CharField('完整路径', max_length=150, default='')
    file_path = models.FileField(upload_to=file_upload_to)
    createDate = models.DateTimeField('创建时间', auto_now_add=True)

class UploadMIL(models.Model):
    def file_upload_to(instance, filename):
        return '{0}/{filename}'.format(instance.fullpath, filename=filename)

    fullpath = models.CharField('完整路径', max_length=150)
    file_path = models.FileField(upload_to=file_upload_to)
    createDate = models.DateTimeField('创建时间', auto_now_add=True)


class uploadImgandVideo(models.Model):
    def file_upload_to(instance, filename):
        return '{0}/{filename}'.format(instance.fullpath, filename=filename)

    fullpath = models.CharField('完整路径', max_length=150)
    file_path = models.FileField(upload_to=file_upload_to)
    createDate = models.DateTimeField('创建时间', auto_now_add=True)