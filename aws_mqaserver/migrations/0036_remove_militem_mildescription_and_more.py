# Generated by Django 4.1.4 on 2023-02-20 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aws_mqaserver', '0035_remove_milscoreitem_audititemid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='militem',
            name='MILDescription',
        ),
        migrations.RemoveField(
            model_name='milscoreitem',
            name='part',
        ),
    ]
