# Generated by Django 4.1.4 on 2023-01-13 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_mqaserver', '0024_alter_lineconfig_lob'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='militem',
            name='process',
        ),
        migrations.AddField(
            model_name='militem',
            name='processCategory',
            field=models.CharField(max_length=50, null=True, verbose_name='processCategory'),
        ),
    ]
