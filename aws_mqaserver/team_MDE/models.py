from django.db import models

class MDELine(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=True, max_length=50)
    productLine = models.CharField('productLine', null=True, max_length=50)
    project = models.CharField('project', null=True, max_length=50)
    checkListId = models.BigIntegerField('checkListId', null=True)
    class Meta:
        db_table = 't_mde_line'

class MDECheckList(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    updateTime = models.DateTimeField(null=True)
    createTime = models.DateTimeField(null=True)
    updaterId = models.BigIntegerField('updaterId', null=True)
    updater = models.CharField('updater', null=True, max_length=50)
    class Meta:
        db_table = 't_mde_check_list'

class MDECheckListItem(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    checkListId = models.BigIntegerField(null=False)
    sn = models.IntegerField('SN', null=False)
    station = models.CharField('Station', null=False, max_length=99)
    process = models.CharField('Process', null=False, max_length=99)
    productLine = models.CharField('Product line', null=False, max_length=99)
    project = models.CharField('Project', null=False, max_length=99)
    checkItem = models.CharField('Check Item', null=False, max_length=999)
    USL = models.FloatField('USL', null=False)
    LSL = models.FloatField('LSL', null=False)
    class Meta:
        db_table = 't_mde_check_list_item'