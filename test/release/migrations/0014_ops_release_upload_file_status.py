# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-08 03:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0013_auto_20180413_0330'),
    ]

    operations = [
        migrations.AddField(
            model_name='ops_release',
            name='upload_file_status',
            field=models.TextField(blank=True),
        ),
    ]
