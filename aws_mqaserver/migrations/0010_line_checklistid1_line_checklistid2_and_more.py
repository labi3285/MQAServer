# Generated by Django 4.1.4 on 2023-01-04 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_mqaserver', '0009_audititem_donecount_audititem_failcount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='line',
            name='checkListId1',
            field=models.BigIntegerField(null=True, verbose_name='checkListId1'),
        ),
        migrations.AddField(
            model_name='line',
            name='checkListId2',
            field=models.BigIntegerField(null=True, verbose_name='checkListId2'),
        ),
        migrations.AddField(
            model_name='line',
            name='checkListId3',
            field=models.BigIntegerField(null=True, verbose_name='checkListId3'),
        ),
    ]