# Generated by Django 4.1.4 on 2023-01-16 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_mqaserver', '0025_remove_militem_process_militem_processcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='audititem',
            name='auditRemark',
            field=models.CharField(max_length=255, null=True, verbose_name='auditRemark'),
        ),
        migrations.AddField(
            model_name='audititem',
            name='crossDays',
            field=models.IntegerField(null=True, verbose_name='crossDays'),
        ),
        migrations.AddField(
            model_name='kappaitem',
            name='auditRemark',
            field=models.CharField(max_length=255, null=True, verbose_name='auditRemark'),
        ),
        migrations.AddField(
            model_name='kappaitem',
            name='crossDays',
            field=models.IntegerField(null=True, verbose_name='crossDays'),
        ),
        migrations.AddField(
            model_name='obaitem',
            name='auditRemark',
            field=models.CharField(max_length=255, null=True, verbose_name='auditRemark'),
        ),
        migrations.AddField(
            model_name='obaitem',
            name='crossDays',
            field=models.IntegerField(null=True, verbose_name='crossDays'),
        ),
    ]
