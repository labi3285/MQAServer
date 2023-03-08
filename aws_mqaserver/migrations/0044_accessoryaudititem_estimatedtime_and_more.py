# Generated by Django 4.1.4 on 2023-03-08 15:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aws_mqaserver', '0043_obaitemscorelossitem_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='accessoryaudititem',
            name='estimatedTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accessoryaudititemcheckitemdestructive',
            name='estimatedTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accessoryaudititemcheckitemglue',
            name='estimatedTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accessoryaudititemcheckitemgluepoint',
            name='estimatedTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
