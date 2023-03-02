from django.db import models
# import os
# import uuid

class AuditType():
    Module = '1'
    Enclosure = '2'
    AudioHome = '3'

class CheckType():
    Module = 'Module'
    Enclosure = 'Enclosure'
    ORT = 'ORT'
    # KAPPA = 4
    # OBA = 5

class ObserveType():
    Cosmetic = 'Cosmetic'
    Surface = 'Surface'

class User(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    team = models.CharField(null=False, max_length=99)
    icon = models.CharField(null=True, max_length=255)
    account = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=32)
    lob = models.CharField(null=True, max_length=999)
    role = models.CharField(max_length=50)
    status = models.SmallIntegerField(default=1)
    createTime = models.DateTimeField(null=True)
    class Meta:
        db_table = 't_sa_user'
    
class Line(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=True, max_length=50)
    productLine = models.CharField('productLine', null=True, max_length=50)
    project = models.CharField('project', null=True, max_length=50)
    part = models.CharField('part', null=True, max_length=50)    
    auditType = models.CharField('auditType', null=False, max_length=999)
    checkListId_Module = models.BigIntegerField('checkListId_Module', null=True)
    checkListId_Enclosure = models.BigIntegerField('checkListId_Enclosure', null=True)
    checkListId_ORT = models.BigIntegerField('checkListId_ORT', null=True)
    class Meta:
        db_table = 't_sa_line'

class LineConfig(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    lob = models.CharField('lob', null=True, max_length=50)
    site = models.CharField('site', null=True, max_length=50)
    productLine = models.CharField('productLine', null=True, max_length=50)
    project = models.CharField('project', null=True, max_length=50)
    part = models.CharField('part', null=True, max_length=50)
    domain = models.CharField('domain', null=False, max_length=50)
    data = models.TextField('data', null=False)
    class Meta:
        db_table = 't_sa_line_config'
        
class CheckList(models.Model):
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
        db_table = 't_sa_check_list'
        
class CheckListItemModule(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    checkListId = models.BigIntegerField(null=False)
    sn = models.IntegerField('sn', null=False)
    mainProcess = models.CharField('mainProcess', null=False, max_length=255)
    subProcess = models.CharField('subProcess', null=False, max_length=255)
    ifCtq = models.BooleanField('ifCtq', null=False)
    measurementEquipment = models.CharField('measurementEquipment', null=False, max_length=255)
    LSL = models.CharField('LSL', null=False, max_length=255)
    USL = models.CharField('USL', null=False, max_length=255)
    LCL = models.CharField('LCL', null=False, max_length=255)
    UCL = models.CharField('UCL', null=False, max_length=255)
    checkItem = models.CharField('checkItem', null=False, max_length=999)
    sampleUnit = models.CharField('sampleUnit', null=False, max_length=255)
    sampleSize = models.CharField('sampleSize', null=False, max_length=255)
    realSampleSize = models.CharField('realSampleSize', null=False, max_length=255)
    frenquencyBasis = models.CharField('frenquencyBasis', null=False, max_length=255)
    controlType = models.CharField('frenquencyBasis', null=False, max_length=255)
    controlMethod = models.CharField('controlMethod', null=False, max_length=255)
    controlCriteria = models.CharField('controlCriteria', null=False, max_length=999)
    responsePlan = models.CharField('responsePlan', null=False, max_length=999)
    sopNo = models.CharField('sopNo', null=False, max_length=99)
    auditSampleSize = models.CharField('auditSampleSize', null=False, max_length=255)
    disScore = models.IntegerField('disScore', null=True)
    disTimes = models.IntegerField('disTimes', null=True)
    skip = models.BooleanField('skip', null=True)
    class Meta:
        db_table = 't_sa_check_list_item_module'
        
class CheckListItemEnclosure(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    checkListId = models.BigIntegerField(null=False)
    sn = models.IntegerField('sn', null=False)
    area = models.CharField('area', null=True, max_length=255)
    mainProcess = models.CharField('mainProcess', null=False, max_length=255)
    subProcess = models.CharField('subProcess', null=False, max_length=255)
    checkItems = models.TextField('checkItems', null=False)
    samplingSize = models.CharField('samplingSize', null=False, max_length=999)
    realSampleSize = models.CharField('realSampleSize', null=False, max_length=999)
    lookingFor = models.CharField('lookingFor', null=False, max_length=4999)
    recordsFindings = models.CharField('recordsFindings', null=False, max_length=999)
    result = models.CharField('result', null=False, max_length=99)
    auditSampleSize = models.CharField('auditSampleSize', null=False, max_length=255)
    disScore = models.IntegerField('disScore', null=True)
    disTimes = models.IntegerField('disTimes', null=True)
    skip = models.BooleanField('skip', null=True)
    class Meta:
        db_table = 't_sa_check_list_item_enclosure'
        
class CheckListItemORT(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    checkListId = models.BigIntegerField(null=False)
    sn = models.IntegerField('sn', null=False)
    project = models.CharField('project', null=False, max_length=255)
    testItem = models.CharField('testItem', null=False, max_length=999)
    testConditionParameter = models.CharField('testConditionParameter', null=False, max_length=999)
    equipment = models.CharField('Equipment', null=False, max_length=255)
    fixtureYN = models.CharField('fixtureYN', null=False, max_length=99)
    sampleOrientation = models.CharField('sampleOrientation', null=False, max_length=255)
    recoveryTime = models.CharField('recoveryTime', null=False, max_length=99)
    sampleSize = models.CharField('sampleSize', null=False, max_length=99)
    samplingFreq = models.CharField('samplingFreq', null=False, max_length=99)
    duration = models.CharField('duration', null=False, max_length=99)
    readPoint = models.CharField('readPoint', null=False, max_length=99)
    passFailCriteria = models.CharField('passFailCriteria', null=False, max_length=999)
    OCAP = models.CharField('OCAP', null=False, max_length=999)
    result = models.CharField('result', null=False, max_length=99)
    disScore = models.IntegerField('disScore', null=True)
    disTimes = models.IntegerField('disTimes', null=True)
    skip = models.BooleanField('skip', null=True)
    class Meta:
        db_table = 't_sa_check_list_item_ort'


# One AuditItem stand for one Audit,
# This is a rough model with all audit items and findings packed in json
class AuditItem(models.Model):
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
    updateTime = models.DateTimeField(null=True)
    createTime = models.DateTimeField(null=True)
    auditorId = models.BigIntegerField('auditorId', null=False)
    auditor = models.CharField('auditor', null=False, max_length=50)
    skipCount = models.IntegerField('skipCount', null=False)
    passCount = models.IntegerField('passCount', null=False)
    failCount = models.IntegerField('failCount', null=False)
    doneCount = models.IntegerField('doneCount', null=False)
    totalCount = models.IntegerField('totalCount', null=False)
    findingCount = models.IntegerField('findingCount', null=False)
    class Meta:
        db_table = 't_sa_audit_item'

class AuditItemCheckItemModule(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    checkListId = models.BigIntegerField(null=True)
    auditItemId = models.BigIntegerField(null=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    part = models.CharField('part', null=False, max_length=50)
    checkItem_sn = models.IntegerField('checkItem_sn', null=False)
    checkItem_mainProcess = models.CharField('checkItem_mainProcess', null=False, max_length=255)
    checkItem_subProcess = models.CharField('checkItem_subProcess', null=False, max_length=255)
    checkItem_ifCtq = models.BooleanField('checkItem_ifCtq', null=False)
    checkItem_measurementEquipment = models.CharField('checkItem_measurementEquipment', null=False, max_length=255)
    checkItem_LSL = models.CharField('checkItem_LSL', null=False, max_length=255)
    checkItem_USL = models.CharField('checkItem_USL', null=False, max_length=255)
    checkItem_LCL = models.CharField('checkItem_LCL', null=False, max_length=255)
    checkItem_UCL = models.CharField('checkItem_UCL', null=False, max_length=255)
    checkItem_checkItem = models.CharField('checkItem_checkItem', null=False, max_length=999)
    checkItem_sampleUnit = models.CharField('checkItem_sampleUnit', null=False, max_length=255)
    checkItem_sampleSize = models.CharField('checkItem_sampleSize', null=False, max_length=255)
    checkItem_frenquencyBasis = models.CharField('checkItem_frenquencyBasis', null=False, max_length=255)
    checkItem_controlType = models.CharField('checkItem_controlType', null=False, max_length=255)
    checkItem_controlMethod = models.CharField('checkItem_controlMethod', null=False, max_length=255)
    checkItem_controlCriteria = models.CharField('checkItem_controlCriteria', null=False, max_length=999)
    checkItem_responsePlan = models.CharField('checkItem_responsePlan', null=False, max_length=999)
    checkItem_sopNo = models.CharField('checkItem_sopNo', null=False, max_length=99)
    checkItem_auditSampleSize = models.CharField('checkItem_auditSampleSize', null=False, max_length=255)
    checkItem_disScore = models.IntegerField('checkItem_disScore', null=True)
    checkItem_disTimes = models.IntegerField('checkItem_disTimes', null=True)
    checkItem_skip = models.BooleanField('checkItem_skip', null=True)
    peopleTrain = models.CharField('peopleTrain', null=True, max_length=255)
    machineMaintenance = models.CharField('machineMaintenance', null=True, max_length=255)
    onsiteVerify = models.CharField('onsiteVerify', null=True, max_length=255)
    materialHandling = models.CharField('materialHandling', null=True, max_length=255)
    environmentSetting = models.CharField('environmentSetting', null=True, max_length=255)
    workshopLineMachine = models.CharField('workshopLineMachine', null=True, max_length=255)
    checkResult = models.CharField('checkResult', null=True, max_length=255)
    result = models.CharField('result', null=True, max_length=255)
    findings = models.TextField('findings', null=True)
    hasFindings = models.BooleanField('hasFindings', null=False)
    isSkip = models.BooleanField('isSkip', null=False)
    isDone = models.BooleanField('isDone', null=False)
    status = models.CharField('status', null=True, max_length=50)
    uploadTime = models.DateTimeField('uploadTime', null=False)
    createTime = models.DateTimeField(null=True)
    auditorId = models.BigIntegerField('auditorId', null=False)
    auditor = models.CharField('auditor', null=False, max_length=50)
    class Meta:
        db_table = 't_sa_audit_item_check_item_module'

class AuditItemCheckItemEnclosure(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    checkListId = models.BigIntegerField(null=True)
    auditItemId = models.BigIntegerField(null=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    part = models.CharField('part', null=False, max_length=50)
    checkItem_sn = models.IntegerField('checkItem_sn', null=False)
    checkItem_area = models.CharField('checkItem_area', null=True, max_length=255)
    checkItem_mainProcess = models.CharField('checkItem_mainProcess', null=False, max_length=255)
    checkItem_subProcess = models.CharField('checkItem_subProcess', null=False, max_length=255)
    checkItem_checkItems = models.TextField('checkItem_checkItems', null=False)
    checkItem_samplingSize = models.CharField('checkItem_samplingSize', null=False, max_length=999)
    checkItem_lookingFor = models.CharField('checkItem_lookingFor', null=False, max_length=4999)
    checkItem_recordsFindings = models.CharField('checkItem_recordsFindings', null=False, max_length=999)
    checkItem_auditSampleSize = models.CharField('checkItem_auditSampleSize', null=False, max_length=255)
    checkItem_disScore = models.IntegerField('checkItem_disScore', null=True)
    checkItem_disTimes = models.IntegerField('checkItem_disTimes', null=True)
    checkItem_skip = models.BooleanField('checkItem_skip', null=True)
    records = models.CharField('records', null=True, max_length=999)
    result = models.CharField('result', null=True, max_length=255)
    findings = models.TextField('findings', null=True)
    hasFindings = models.BooleanField('hasFindings', null=False)
    isSkip = models.BooleanField('isSkip', null=False)
    isDone = models.BooleanField('isDone', null=False)
    status = models.CharField('status', null=True, max_length=50)
    uploadTime = models.DateTimeField('uploadTime', null=False)
    createTime = models.DateTimeField(null=True)
    auditorId = models.BigIntegerField('auditorId', null=False)
    auditor = models.CharField('auditor', null=False, max_length=50)
    class Meta:
        db_table = 't_sa_audit_item_check_item_enclosure'

class AuditItemCheckItemORT(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    checkListId = models.BigIntegerField(null=True)
    auditItemId = models.BigIntegerField(null=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    part = models.CharField('part', null=False, max_length=50)
    checkItem_sn = models.IntegerField('checkItem_sn', null=False)
    checkItem_project = models.CharField('checkItem_project', null=False, max_length=255)
    checkItem_testItem = models.CharField('checkItem_testItem', null=False, max_length=999)
    checkItem_testConditionParameter = models.CharField('checkItem_testConditionParameter', null=False, max_length=999)
    checkItem_equipment = models.CharField('checkItem_equipment', null=False, max_length=255)
    checkItem_fixtureYN = models.CharField('checkItem_fixtureYN', null=False, max_length=99)
    checkItem_sampleOrientation = models.CharField('checkItem_sampleOrientation', null=False, max_length=255)
    checkItem_recoveryTime = models.CharField('checkItem_recoveryTime', null=False, max_length=99)
    checkItem_sampleSize = models.CharField('checkItem_sampleSize', null=False, max_length=99)
    checkItem_samplingFreq = models.CharField('checkItem_samplingFreq', null=False, max_length=99)
    checkItem_duration = models.CharField('checkItem_duration', null=False, max_length=99)
    checkItem_readPoint = models.CharField('checkItem_readPoint', null=False, max_length=99)
    checkItem_passFailCriteria = models.CharField('checkItem_passFailCriteria', null=False, max_length=999)
    checkItem_OCAP = models.CharField('checkItem_OCAP', null=False, max_length=999)
    checkItem_disScore = models.IntegerField('checkItem_disScore', null=True)
    checkItem_disTimes = models.IntegerField('checkItem_disTimes', null=True)
    checkItem_skip = models.BooleanField('checkItem_skip', null=True)
    result = models.CharField('result', null=True, max_length=255)
    findings = models.TextField('findings', null=True)
    hasFindings = models.BooleanField('hasFindings', null=False)
    isSkip = models.BooleanField('isSkip', null=False)
    isDone = models.BooleanField('isDone', null=False)
    status = models.CharField('status', null=True, max_length=50)
    uploadTime = models.DateTimeField('uploadTime', null=False)
    createTime = models.DateTimeField(null=True)
    auditorId = models.BigIntegerField('auditorId', null=False)
    auditor = models.CharField('auditor', null=False, max_length=50)
    class Meta:
        db_table = 't_sa_audit_item_check_item_ort'

class KAPPAItem(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    part = models.CharField('part', null=False, max_length=50)
    type = models.CharField('type', null=False, max_length=50)
    year = models.SmallIntegerField('year', null=False)
    highlight = models.CharField('highlight', null=False, max_length=255)
    scoreLossItem = models.CharField('scoreLossItem', null=False, max_length=999)
    score = models.FloatField('score', null=False)
    kappaSkillMatrixScores = models.CharField('kappaSkillMatrixScores', null=False, max_length=999)
    kappaSkillMatrixAverageScore = models.FloatField('kappaSkillMatrixAverageScore', null=False)
    beginTime = models.DateTimeField('beginTime', null=False)
    endTime = models.DateTimeField('endTime', null=False)
    updateTime = models.DateTimeField(null=True)
    createTime = models.DateTimeField(null=True)
    auditorId = models.BigIntegerField('auditorId', null=False)
    auditor = models.CharField('auditor', null=False, max_length=50)
    class Meta:
        db_table = 't_sa_kappa_item'

class KAPPAItemScoreLossItem(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    kappaItemId = models.BigIntegerField(null=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    part = models.CharField('part', null=False, max_length=50)
    type = models.CharField('type', null=False, max_length=50)
    year = models.SmallIntegerField('year', null=False)
    item = models.CharField('item', null=False, max_length=30)
    breakDown = models.CharField('breakDown', null=False, max_length=255)
    scoreLoss = models.FloatField('scoreLoss', null=False)
    createTime = models.DateTimeField(null=True)
    auditorId = models.BigIntegerField('auditorId', null=False)
    auditor = models.CharField('auditor', null=False, max_length=50)
    class Meta:
        db_table = 't_sa_kappa_item_score_loss_item'

class KAPPAItemKappaSkillScoreItem(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    kappaItemId = models.BigIntegerField(null=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    part = models.CharField('part', null=False, max_length=50)
    type = models.CharField('type', null=False, max_length=50)
    year = models.SmallIntegerField('year', null=False)
    name = models.CharField('name', null=False, max_length=99)
    position = models.CharField('position', null=False, max_length=99)
    score = models.FloatField('score', null=False)
    judgement = models.CharField('name', null=False, max_length=50)
    createTime = models.DateTimeField('createTime', null=False)
    auditorId = models.BigIntegerField('auditorId', null=False)
    auditor = models.CharField('auditor', null=False, max_length=50)
    class Meta:
        db_table = 't_sa_kappa_item_kappa_skill_score_item'

class OBAItem(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    part = models.CharField('part', null=False, max_length=50)
    type = models.CharField('type', null=False, max_length=50)
    year = models.SmallIntegerField('year', null=False)
    highlight = models.CharField('highlight', null=False, max_length=255)
    scoreLossItem = models.CharField('scoreLossItem', null=False, max_length=999)
    score = models.FloatField('score', null=False)
    findings = models.CharField('findings', null=False, max_length=999)
    findingsCount = models.IntegerField('findingsCount', null=False)
    beginTime = models.DateTimeField('beginTime', null=False)
    endTime = models.DateTimeField('endTime', null=False)
    updateTime = models.DateTimeField(null=True)
    createTime = models.DateTimeField(null=True)
    auditorId = models.BigIntegerField('auditorId', null=False)
    auditor = models.CharField('auditor', null=False, max_length=50)
    class Meta:
        db_table = 't_sa_oba_item'

class OBAItemScoreLossItem(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    obaItemId = models.BigIntegerField(null=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    part = models.CharField('part', null=False, max_length=50)
    type = models.CharField('type', null=False, max_length=50)
    year = models.SmallIntegerField('year', null=False)
    item = models.CharField('item', null=False, max_length=30)
    breakDown = models.CharField('breakDown', null=False, max_length=255)
    scoreLoss = models.FloatField('scoreLoss', null=False)
    createTime = models.DateTimeField(null=True)
    auditorId = models.BigIntegerField('auditorId', null=False)
    auditor = models.CharField('auditor', null=False, max_length=50)
    class Meta:
        db_table = 't_sa_oba_item_score_loss_item'

class OBAItemMILItem(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    obaItemId = models.BigIntegerField(null=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    part = models.CharField('part', null=False, max_length=50)
    type = models.CharField('type', null=False, max_length=50)
    year = models.SmallIntegerField('year', null=False)
    vendor = models.CharField('vendor', null=False, max_length=50)
    month = models.SmallIntegerField('month', null=False)
    quarter = models.CharField('quarter', null=False, max_length=9)
    auditDate = models.DateTimeField('auditDate', null=False)
    severity = models.CharField('severity', null=False, max_length=50)
    findings = models.CharField('severity', null=False, max_length=999)
    createTime = models.DateTimeField('createTime', null=False)
    auditorId = models.BigIntegerField('auditorId', null=False)
    auditor = models.CharField('auditor', null=False, max_length=50)
    class Meta:
        db_table = 't_sa_oba_item_mil_item'

class MILItem(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    auditItemId = models.BigIntegerField('auditItemId', null=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    part = models.CharField('part', null=False, max_length=50)
    type = models.CharField('type', null=False, max_length=50)
    sn = models.IntegerField('sn', null=True)
    year = models.SmallIntegerField('year', null=False)
    month = models.SmallIntegerField('month', null=False)
    week = models.SmallIntegerField('week', null=False)
    day = models.SmallIntegerField('day', null=False)
    quarter = models.SmallIntegerField('quarter', null=False)
    auditType = models.CharField('auditType', null=False, max_length=99)
    vendor = models.CharField('vendor', null=False, max_length=50)
    factory = models.CharField('factory', null=False, max_length=50)
    projectPart = models.CharField('projectPart', null=False, max_length=50)
    processCategory = models.CharField('processCategory', null=True, max_length=50)
    line = models.CharField('line', null=True, max_length=50)
    station = models.CharField('station', null=True, max_length=50)
    stage = models.CharField('stage', null=True, max_length=50)
    auditTimes = models.SmallIntegerField('auditTimes', null=True)
    productCategory = models.CharField('productCategory', null=True, max_length=50)
    byAuditCategory = models.CharField('byAuditCategory', null=True, max_length=50)
    issueCategory = models.CharField('issueCategory', null=True, max_length=50)
    subCategory = models.CharField('subCategory', null=True, max_length=50)
    issueBrief = models.CharField('issueBrief', null=True, max_length=255)
    keywords = models.CharField('keywords', null=True, max_length=255)
    status = models.SmallIntegerField('status', null=True)
    programRelated = models.CharField('programRelated', null=True, max_length=99)
    severity = models.CharField('severity', null=True, max_length=50)
    findings = models.CharField('findings', null=True, max_length=255)
    containmentAction = models.CharField('containmentAction', null=True, max_length=255)
    failureAnalysisRootCause = models.CharField('failureAnalysisRootCause', null=True, max_length=255)
    correctiveAction = models.CharField('correctiveAction', null=True, max_length=255)
    department = models.CharField('department', null=True, max_length=50)
    vendorDRI = models.CharField('vendorDri', null=True, max_length=50)
    errorProofCategory = models.CharField('errorProofCategory', null=True, max_length=50)
    errorProof = models.CharField('errorProof', null=True, max_length=255)
    cheatingCategory = models.CharField('cheatingCategory', null=True, max_length=50)
    cheatingSubcategory = models.CharField('cheatingSubcategory', null=True, max_length=50)
    cheatingPattern = models.CharField('cheatingPattern', null=True, max_length=255)
    emailDate = models.DateTimeField('emailDate', null=True)
    planClosedDueDate = models.DateTimeField('planClosedDueDate', null=True)
    actualClosedDate = models.DateTimeField('actualClosedDate', null=True)
    dueMonth = models.SmallIntegerField('dueMonth', null=True)
    ifMILResponseDelayed = models.BooleanField('ifMILResponseDelayed', null=True)
    containmentActionDate = models.DateTimeField('containmentActionDate', null=True)
    containmentLTDate = models.DateTimeField('containmentLTDate', null=True)
    ifContainmentDelayed = models.BooleanField('ifContainmentDelayed', null=True)
    FAFinalizedDate = models.DateTimeField('FAFinalizedDate', null=True)
    FAFinalizedLTDate = models.DateTimeField('FAFinalizedLTDate', null=True)
    ifFADelayed = models.BooleanField('ifFADelayed', null=True)
    CAFinalizedDate = models.DateTimeField('CAFinalizedDate', null=True)
    CAFinalizedLTDate = models.DateTimeField('CAFinalizedLTDate', null=True)
    ifCADelayed = models.BooleanField('ifCADelayed', null=True)
    CAClosureDate = models.DateTimeField('CAClosureDate', null=True)
    ifClosureDelayed = models.BooleanField('ifClosureDelayed', null=True)
    FACAScoreByVendorEvaluationGroup = models.CharField('FACAScoreByVendorEvaluationGroup', null=True, max_length=99)
    vendorEvaluationGroupComments = models.CharField('vendorEvaluationGroupComments', null=True, max_length=300)
    appleFirstEvaluationScore = models.CharField('appleFirstEvaluationScore', null=True, max_length=30)
    appleComments = models.CharField('appleComments', null=True, max_length=255)
    FACAReviewTimes = models.SmallIntegerField('FACAReviewTimes', null=True)
    repeatIssue = models.BooleanField('repeatIssue', null=True)
    repeatTime = models.DateTimeField('repeatTime', null=True)
    auditBlockedPartsQty = models.CharField('auditBlockedPartsQty', null=True, max_length=99)
    scrapedQty = models.CharField('scrapedQty', null=True, max_length=99)
    containments = models.TextField('containments', null=True)
    FAs = models.TextField('FAs', null=True)
    CAs = models.TextField('CAs', null=True)
    highlight = models.BooleanField('highlight', null=True)
    highlightDescription = models.CharField('highlightDescription', null=True, max_length=300)
    auditorId = models.BigIntegerField('auditorId', null=True)
    auditor = models.CharField('auditor', null=True, max_length=32)
    createTime = models.DateTimeField(null=True)
    FA = models.CharField('FA', null=True, max_length=500)
    CA = models.CharField('CA', null=True, max_length=500)
    class Meta:
        db_table = 't_sa_mil_item'

class MILScoreItem(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    lob = models.CharField('lob', null=False, max_length=50)
    site = models.CharField('site', null=False, max_length=50)
    productLine = models.CharField('productLine', null=False, max_length=50)
    project = models.CharField('project', null=False, max_length=50)
    type = models.CharField('type', null=False, max_length=50)
    year = models.SmallIntegerField('year', null=False)
    month = models.SmallIntegerField('month', null=False)
    quarter = models.SmallIntegerField('quarter', null=False)
    vendor = models.CharField('vendor', null=False, max_length=50)
    auditType = models.CharField('auditType', null=False, max_length=99)
    score = models.FloatField('score', null=False)
    range = models.FloatField('range', null=False)
    class Meta:
        db_table = 't_sa_mil_score_item'

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

    fullpath = models.CharField(max_length=150)
    #savepath = models.CharField('完整路径', max_length=150, default='')
    file_path = models.FileField(upload_to=file_upload_to)
    createDate = models.DateTimeField('创建时间', auto_now_add=True)


class uploadImgandVideo(models.Model):
    def file_upload_to(instance, filename):
        return '{0}/{filename}'.format(instance.fullpath, filename=filename)

    fullpath = models.CharField('完整路径', max_length=150)
    file_path = models.FileField(upload_to=file_upload_to)
    createDate = models.DateTimeField('创建时间', auto_now_add=True)

from aws_mqaserver.team_MDE.models import *
from aws_mqaserver.team_Accessory.models import *
from aws_mqaserver.team_Display.models import *
from aws_mqaserver.team_SIP.models import *
