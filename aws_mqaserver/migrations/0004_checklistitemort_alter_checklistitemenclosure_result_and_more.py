# Generated by Django 4.1.4 on 2022-12-28 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_mqaserver', '0003_checklist_checklistitemenclosure_checklistitemmodule_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckListItemORT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('checkListId', models.BigIntegerField()),
                ('sn', models.IntegerField(verbose_name='sn')),
                ('project', models.CharField(max_length=255, verbose_name='project')),
                ('testItem', models.CharField(max_length=999, verbose_name='testItem')),
                ('testConditionParameter', models.CharField(max_length=999, verbose_name='testConditionParameter')),
                ('equipment', models.CharField(max_length=255, verbose_name='Equipment')),
                ('fixtureYN', models.CharField(max_length=99, verbose_name='fixtureYN')),
                ('sampleOrientation', models.CharField(max_length=255, verbose_name='sampleOrientation')),
                ('recoveryTime', models.CharField(max_length=99, verbose_name='recoveryTime')),
                ('sampleSize', models.CharField(max_length=99, verbose_name='sampleSize')),
                ('samplingFreq', models.CharField(max_length=99, verbose_name='samplingFreq')),
                ('duration', models.CharField(max_length=99, verbose_name='duration')),
                ('readPoint', models.CharField(max_length=99, verbose_name='readPoint')),
                ('passFailCriteria', models.CharField(max_length=999, verbose_name='passFailCriteria')),
                ('OCAP', models.CharField(max_length=999, verbose_name='OCAP')),
                ('result', models.CharField(max_length=99, verbose_name='result')),
            ],
            options={
                'db_table': 't_sa_check_list_item_ort',
            },
        ),
        migrations.AlterField(
            model_name='checklistitemenclosure',
            name='result',
            field=models.CharField(max_length=99, verbose_name='result'),
        ),
        migrations.AlterField(
            model_name='checklistitemmodule',
            name='result',
            field=models.CharField(max_length=99, verbose_name='result'),
        ),
    ]
