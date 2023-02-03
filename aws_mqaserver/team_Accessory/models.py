from django.db import models

class AccessoryCheckType():
    Glue = "Glue"
    Destructive = "Destructive"

class AccessoryLine(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=True, max_length=50)
    productLine = models.CharField('productLine', null=True, max_length=50)
    project = models.CharField('project', null=True, max_length=50)
    part = models.CharField('part', null=True, max_length=50)
    checkListId_Glue = models.BigIntegerField('checkListId_Glue', null=True)
    checkListId_Destructive = models.BigIntegerField('checkListId_Destructive', null=True)
    class Meta:
        db_table = 't_accessory_line'

class AccessoryCheckList(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    part = models.CharField('part', null=False, max_length=50)
    type = models.CharField('type', null=False, max_length=50)
    updateTime = models.DateTimeField(null=True)
    createTime = models.DateTimeField(null=True)
    updaterId = models.BigIntegerField('updaterId', null=True)
    updater = models.CharField('updater', null=True, max_length=50)
    class Meta:
        db_table = 't_accessory_check_list'

class AccessoryCheckListItemGlue(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    checkListId = models.BigIntegerField(null=False)
    sn = models.IntegerField('sn', null=False)
    theClass = models.CharField('theClass', null=False, max_length=99)
    lineShift = models.CharField('lineShift', null=False, max_length=99)
    site = models.CharField('site', null=False, max_length=99)
    projects = models.CharField('projects', null=False, max_length=99)
    item = models.CharField('item', null=False, max_length=255)
    unit = models.CharField('unit', null=False, max_length=255)
    LSL = models.CharField('LSL', null=False, max_length=99)
    USL = models.CharField('USL', null=False, max_length=99)
    class Meta:
        db_table = 't_accessory_check_list_item_glue'
class AccessoryCheckListItemDestructive(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    checkListId = models.BigIntegerField(null=False)
    sn = models.IntegerField('sn', null=False)
    theClass = models.CharField('theClass', null=False, max_length=99)
    lineShift = models.CharField('lineShift', null=False, max_length=99)
    site = models.CharField('site', null=False, max_length=99)
    projects = models.CharField('projects', null=False, max_length=99)
    item = models.CharField('item', null=False, max_length=255)
    unit = models.CharField('unit', null=False, max_length=255)
    LSL = models.CharField('LSL', null=False, max_length=99)
    USL = models.CharField('USL', null=True, max_length=99)
    class Meta:
        db_table = 't_accessory_check_list_item_destructive'

class AccessoryAuditItem(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    part = models.CharField('part', null=False, max_length=50)
    type = models.CharField('type', null=False, max_length=50)
    rawJson = models.TextField('rawJson', null=False)
    beginTime = models.DateTimeField('beginTime', null=False)
    endTime = models.DateTimeField('endTime', null=False)
    uploadTime = models.DateTimeField('uploadTime', null=False)
    crossDays = models.IntegerField('crossDays', null=True)
    auditRemark = models.CharField('auditRemark', null=True, max_length=255)
    updateTime = models.DateTimeField(null=True)
    createTime = models.DateTimeField(null=True)
    auditorId = models.BigIntegerField('auditorId', null=False)
    auditor = models.CharField('auditor', null=False, max_length=50)
    passCount = models.IntegerField('passCount', null=False)
    failCount = models.IntegerField('failCount', null=False)
    doneCount = models.IntegerField('doneCount', null=False)
    totalCount = models.IntegerField('totalCount', null=False)
    class Meta:
        db_table = 't_accessory_audit_item'

class AccessoryAuditItemCheckItemGlue(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    checkListId = models.BigIntegerField(null=True)
    auditItemId = models.BigIntegerField(null=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    part = models.CharField('part', null=False, max_length=50)
    checkItem_sn = models.IntegerField('checkItem_sn', null=False)
    checkItem_theClass = models.CharField('checkItem_theClass', null=False, max_length=99)
    checkItem_lineShift = models.CharField('checkItem_lineShift', null=False, max_length=99)
    checkItem_site = models.CharField('checkItem_site', null=False, max_length=99)
    checkItem_projects = models.CharField('checkItem_projects', null=False, max_length=99)
    checkItem_item = models.CharField('checkItem_item', null=False, max_length=255)
    checkItem_unit = models.CharField('checkItem_unit', null=False, max_length=255)
    checkItem_LSL = models.CharField('checkItem_LSL', null=False, max_length=99)
    checkItem_USL = models.CharField('checkItem_USL', null=False, max_length=99)
    passCount = models.IntegerField('passCount', null=False)
    failCount = models.IntegerField('failCount', null=False)
    totalCount = models.IntegerField('totalCount', null=False)
    isDone = models.BooleanField('isDone', null=False)
    status = models.CharField('status', null=True, max_length=50)
    uploadTime = models.DateTimeField('uploadTime', null=False)
    createTime = models.DateTimeField(null=True)
    auditorId = models.BigIntegerField('auditorId', null=False)
    auditor = models.CharField('auditor', null=False, max_length=50)
    class Meta:
        db_table = 't_accessory_audit_item_check_item_glue'
class AccessoryAuditItemCheckItemGluePoint(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    checkListId = models.BigIntegerField(null=True)
    auditItemId = models.BigIntegerField(null=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    part = models.CharField('part', null=False, max_length=50)
    checkItem_sn = models.IntegerField('checkItem_sn', null=False)
    checkItem_theClass = models.CharField('checkItem_theClass', null=False, max_length=99)
    checkItem_lineShift = models.CharField('checkItem_lineShift', null=False, max_length=99)
    checkItem_site = models.CharField('checkItem_site', null=False, max_length=99)
    checkItem_projects = models.CharField('checkItem_projects', null=False, max_length=99)
    checkItem_item = models.CharField('checkItem_item', null=False, max_length=255)
    checkItem_unit = models.CharField('checkItem_unit', null=False, max_length=255)
    checkItem_LSL = models.CharField('checkItem_LSL', null=False, max_length=99)
    checkItem_USL = models.CharField('checkItem_USL', null=False, max_length=99)
    before = models.FloatField('before', null=False)
    after = models.FloatField('after', null=False)
    result = models.FloatField('result', null=False)
    outOfSpec = models.BooleanField('outOfSpec', null=False)
    uploadTime = models.DateTimeField('uploadTime', null=False)
    createTime = models.DateTimeField(null=True)
    auditorId = models.BigIntegerField('auditorId', null=False)
    auditor = models.CharField('auditor', null=False, max_length=50)
    class Meta:
        db_table = 't_accessory_audit_item_check_item_glue_point'

class AccessoryAuditItemCheckItemDestructive(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    checkListId = models.BigIntegerField(null=True)
    auditItemId = models.BigIntegerField(null=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    part = models.CharField('part', null=False, max_length=50)
    checkItem_sn = models.IntegerField('checkItem_sn', null=False)
    checkItem_theClass = models.CharField('checkItem_theClass', null=False, max_length=99)
    checkItem_lineShift = models.CharField('checkItem_lineShift', null=False, max_length=99)
    checkItem_site = models.CharField('checkItem_site', null=False, max_length=99)
    checkItem_projects = models.CharField('checkItem_projects', null=False, max_length=99)
    checkItem_item = models.CharField('checkItem_item', null=False, max_length=255)
    checkItem_unit = models.CharField('checkItem_unit', null=False, max_length=255)
    checkItem_LSL = models.CharField('checkItem_LSL', null=False, max_length=99)
    checkItem_USL = models.CharField('checkItem_USL', null=True, max_length=99)
    passCount = models.IntegerField('passCount', null=False)
    failCount = models.IntegerField('failCount', null=False)
    totalCount = models.IntegerField('totalCount', null=False)
    isDone = models.BooleanField('isDone', null=False)
    status = models.CharField('status', null=True, max_length=50)
    uploadTime = models.DateTimeField('uploadTime', null=False)
    createTime = models.DateTimeField(null=True)
    auditorId = models.BigIntegerField('auditorId', null=False)
    auditor = models.CharField('auditor', null=False, max_length=50)
    class Meta:
        db_table = 't_accessory_audit_item_check_item_destructive'
class AccessoryAuditItemCheckItemDestructivePoint(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    checkListId = models.BigIntegerField(null=True)
    auditItemId = models.BigIntegerField(null=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    part = models.CharField('part', null=False, max_length=50)
    checkItem_sn = models.IntegerField('checkItem_sn', null=False)
    checkItem_theClass = models.CharField('checkItem_theClass', null=False, max_length=99)
    checkItem_lineShift = models.CharField('checkItem_lineShift', null=False, max_length=99)
    checkItem_site = models.CharField('checkItem_site', null=False, max_length=99)
    checkItem_projects = models.CharField('checkItem_projects', null=False, max_length=99)
    checkItem_item = models.CharField('checkItem_item', null=False, max_length=255)
    checkItem_unit = models.CharField('checkItem_unit', null=False, max_length=255)
    checkItem_LSL = models.CharField('checkItem_LSL', null=False, max_length=99)
    checkItem_USL = models.CharField('checkItem_USL', null=True, max_length=99)
    result = models.FloatField('result', null=False)
    outOfSpec = models.BooleanField('outOfSpec', null=False)
    uploadTime = models.DateTimeField('uploadTime', null=False)
    createTime = models.DateTimeField(null=True)
    auditorId = models.BigIntegerField('auditorId', null=False)
    auditor = models.CharField('auditor', null=False, max_length=50)
    class Meta:
        db_table = 't_accessory_audit_item_check_item_destructive_point'