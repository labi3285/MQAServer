# Generated by Django 4.1.4 on 2023-01-01 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_mqaserver', '0006_remove_militem_auditorname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='KAPPAItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('lob', models.CharField(max_length=50, verbose_name='lob')),
                ('site', models.CharField(max_length=50, verbose_name='site')),
                ('productLine', models.CharField(max_length=50, verbose_name='productLine')),
                ('project', models.CharField(max_length=50, verbose_name='project')),
                ('part', models.CharField(max_length=50, verbose_name='part')),
                ('type', models.SmallIntegerField(verbose_name='type')),
                ('year', models.SmallIntegerField(verbose_name='year')),
                ('highlight', models.CharField(max_length=255, verbose_name='highlight')),
                ('scoreLossItem', models.CharField(max_length=999, verbose_name='scoreLossItem')),
                ('score', models.FloatField(verbose_name='score')),
                ('kappaSkillMatrixScores', models.CharField(max_length=999, verbose_name='kappaSkillMatrixScores')),
                ('kappaSkillMatrixAverageScore', models.FloatField(verbose_name='kappaSkillMatrixAverageScore')),
                ('beginTime', models.DateTimeField(verbose_name='beginTime')),
                ('endTime', models.DateTimeField(verbose_name='endTime')),
                ('updateTime', models.DateTimeField(null=True)),
                ('createTime', models.DateTimeField(null=True)),
                ('auditorId', models.BigIntegerField(verbose_name='auditorId')),
                ('auditor', models.CharField(max_length=50, verbose_name='auditor')),
            ],
            options={
                'db_table': 't_sa_kappa_item',
            },
        ),
    ]
