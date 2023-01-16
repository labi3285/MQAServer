# Generated by Django 4.1.4 on 2023-01-13 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_mqaserver', '0022_remove_militem_faca_militem_ca_militem_fa'),
    ]

    operations = [
        migrations.CreateModel(
            name='LineConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('team', models.CharField(max_length=99)),
                ('lob', models.CharField(max_length=50, verbose_name='lob')),
                ('site', models.CharField(max_length=50, null=True, verbose_name='site')),
                ('productLine', models.CharField(max_length=50, null=True, verbose_name='productLine')),
                ('project', models.CharField(max_length=50, null=True, verbose_name='project')),
                ('part', models.CharField(max_length=50, null=True, verbose_name='part')),
                ('domain', models.CharField(max_length=50, verbose_name='domain')),
                ('data', models.TextField(verbose_name='data')),
            ],
            options={
                'db_table': 't_sa_line_config',
            },
        ),
    ]