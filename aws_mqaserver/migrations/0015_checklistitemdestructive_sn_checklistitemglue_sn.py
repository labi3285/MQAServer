# Generated by Django 4.1.4 on 2023-01-06 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_mqaserver', '0014_checklistitemdestructive_checklistitemglue_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklistitemdestructive',
            name='sn',
            field=models.IntegerField(default=0, verbose_name='sn'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='checklistitemglue',
            name='sn',
            field=models.IntegerField(default=0, verbose_name='sn'),
            preserve_default=False,
        ),
    ]