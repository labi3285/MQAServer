# Generated by Django 4.1.4 on 2023-01-11 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_mqaserver', '0021_militem_faca_militem_mildescription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='militem',
            name='FACA',
        ),
        migrations.AddField(
            model_name='militem',
            name='CA',
            field=models.CharField(max_length=500, null=True, verbose_name='CA'),
        ),
        migrations.AddField(
            model_name='militem',
            name='FA',
            field=models.CharField(max_length=500, null=True, verbose_name='FA'),
        ),
    ]