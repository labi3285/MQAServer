# Generated by Django 4.1.4 on 2023-02-23 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_mqaserver', '0038_remove_mdeaudititem_donecount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mdeaudititemcheckitem',
            name='value',
            field=models.CharField(max_length=30, null=True, verbose_name='Value'),
        ),
    ]