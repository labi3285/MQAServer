# Generated by Django 4.1.4 on 2023-01-05 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_mqaserver', '0013_audititem_team_checklist_team_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckListItemDestructive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('team', models.CharField(max_length=99)),
                ('checkListId', models.BigIntegerField()),
                ('theClass', models.CharField(max_length=99, verbose_name='theClass')),
                ('lineShift', models.CharField(max_length=99, verbose_name='lineShift')),
                ('site', models.CharField(max_length=99, verbose_name='site')),
                ('projects', models.CharField(max_length=99, verbose_name='projects')),
                ('item', models.CharField(max_length=255, verbose_name='item')),
                ('unit', models.CharField(max_length=255, verbose_name='unit')),
                ('LSL', models.CharField(max_length=99, verbose_name='LSL')),
            ],
            options={
                'db_table': 't_sa_check_list_item_destructive',
            },
        ),
        migrations.CreateModel(
            name='CheckListItemGlue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('team', models.CharField(max_length=99)),
                ('checkListId', models.BigIntegerField()),
                ('theClass', models.CharField(max_length=99, verbose_name='theClass')),
                ('lineShift', models.CharField(max_length=99, verbose_name='lineShift')),
                ('site', models.CharField(max_length=99, verbose_name='site')),
                ('projects', models.CharField(max_length=99, verbose_name='projects')),
                ('item', models.CharField(max_length=255, verbose_name='item')),
                ('glue', models.CharField(max_length=255, verbose_name='glue')),
                ('unit', models.CharField(max_length=255, verbose_name='unit')),
                ('LSL', models.CharField(max_length=99, verbose_name='LSL')),
                ('USL', models.CharField(max_length=99, verbose_name='USL')),
            ],
            options={
                'db_table': 't_sa_check_list_item_glue',
            },
        ),
        migrations.AddField(
            model_name='line',
            name='checkListId10',
            field=models.BigIntegerField(null=True, verbose_name='checkListId10'),
        ),
        migrations.AddField(
            model_name='line',
            name='checkListId11',
            field=models.BigIntegerField(null=True, verbose_name='checkListId11'),
        ),
    ]
