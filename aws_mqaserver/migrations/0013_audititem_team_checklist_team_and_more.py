# Generated by Django 4.1.4 on 2023-01-05 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_mqaserver', '0012_line_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='audititem',
            name='team',
            field=models.CharField(default='MQA', max_length=99),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='checklist',
            name='team',
            field=models.CharField(default='MQA', max_length=99),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='checklistitemenclosure',
            name='team',
            field=models.CharField(default='MQA', max_length=99),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='checklistitemmodule',
            name='team',
            field=models.CharField(default='MQA', max_length=99),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='checklistitemort',
            name='team',
            field=models.CharField(default='MQA', max_length=99),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='kappaitem',
            name='team',
            field=models.CharField(default='MQA', max_length=99),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='militem',
            name='team',
            field=models.CharField(default='MQA', max_length=99),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='obaitem',
            name='team',
            field=models.CharField(default='MQA', max_length=99),
            preserve_default=False,
        ),
    ]
