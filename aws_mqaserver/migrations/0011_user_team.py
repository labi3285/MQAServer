# Generated by Django 4.1.4 on 2023-01-05 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_mqaserver', '0010_line_checklistid1_line_checklistid2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='team',
            field=models.CharField(default='MQA', max_length=99),
            preserve_default=False,
        ),
    ]
