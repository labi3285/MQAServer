# Generated by Django 4.0.1 on 2022-02-21 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MQAServices', '0005_upload_message_alter_upload_file_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='upload',
            name='message',
        ),
        migrations.AlterField(
            model_name='upload',
            name='file_path',
            field=models.FileField(upload_to='History/'),
        ),
    ]
