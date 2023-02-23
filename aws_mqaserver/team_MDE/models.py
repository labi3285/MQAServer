from django.db import models

class MDECheckType():
    Glue = "Glue"
    Destructive = "Destructive"

class MDELine(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=True, max_length=50)
    productLine = models.CharField('productLine', null=True, max_length=50)
    project = models.CharField('project', null=True, max_length=50)
    part = models.CharField('part', null=True, max_length=50)
    checkListId = models.BigIntegerField('checkListId', null=True)
    class Meta:
        db_table = 't_mde_line'

class MDECheckList(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    part = models.CharField('part', null=False, max_length=50)
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
    part = models.CharField('Part', null=False, max_length=99)
    checkItem = models.CharField('Check Item', null=False, max_length=999)
    USL = models.FloatField('USL', null=False)
    LSL = models.FloatField('LSL', null=False)
    class Meta:
        db_table = 't_mde_check_list_item'

class MDEAuditItem(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    part = models.CharField('part', null=False, max_length=50)
    beginTime = models.DateTimeField('beginTime', null=False)
    endTime = models.DateTimeField('endTime', null=False)
    uploadTime = models.DateTimeField('uploadTime', null=False)
    createTime = models.DateTimeField(null=True)
    auditorId = models.BigIntegerField('auditorId', null=False)
    auditor = models.CharField('auditor', null=False, max_length=50)
    okCount = models.IntegerField('okCount', null=False)
    ngCount = models.IntegerField('ngCount', null=False)
    naCount = models.IntegerField('naCount', null=False)
    allCount = models.IntegerField('allCount', null=False)
    score = models.IntegerField('score', null=False)
    class Meta:
        db_table = 't_mde_audit_item'

class MDEAuditItemCheckItem(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    checkListId = models.BigIntegerField(null=True)
    auditItemId = models.BigIntegerField(null=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    part = models.CharField('part', null=False, max_length=50)
    checkItem_sn = models.IntegerField('SN', null=False)
    checkItem_station = models.CharField('Station', null=False, max_length=99)
    checkItem_process = models.CharField('Process', null=False, max_length=99)
    checkItem_productLine = models.CharField('Product line', null=False, max_length=99)
    checkItem_project = models.CharField('Project', null=False, max_length=99)
    checkItem_checkItem = models.CharField('Check Item', null=False, max_length=999)
    checkItem_USL = models.FloatField('USL', null=False)
    checkItem_LSL = models.FloatField('LSL', null=False)
    value = models.CharField('Value', null=True, max_length=30)
    status = models.CharField('status', null=True, max_length=50)
    uploadTime = models.DateTimeField('uploadTime', null=False)
    createTime = models.DateTimeField(null=True)
    auditorId = models.BigIntegerField('auditorId', null=False)
    auditor = models.CharField('auditor', null=False, max_length=50)
    class Meta:
        db_table = 't_mde_audit_item_check_item'