# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-04-13 03:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0012_auto_20180411_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='ops_release',
            name='ops_toback_status',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='ops_release',
            name='toback_user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ops_release',
            name='ops_to_pre_status',
            field=models.BooleanField(default=0),
        ),
    ]