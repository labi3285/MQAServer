# Generated by Django 4.1.4 on 2023-03-01 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws_mqaserver', '0041_alter_mdechecklistitem_lsl'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kappaitemkappaskillscoreitem',
            old_name='obaItemId',
            new_name='kappaItemId',
        ),
        migrations.RenameField(
            model_name='kappaitemscorelossitem',
            old_name='obaItemId',
            new_name='kappaItemId',
        ),
        migrations.AddField(
            model_name='kappaitemscorelossitem',
            name='item',
            field=models.CharField(default='', max_length=30, verbose_name='item'),
            preserve_default=False,
        ),
    ]
