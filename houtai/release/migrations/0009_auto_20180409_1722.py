# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-04-09 09:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0008_auto_20180409_1600'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dba_release',
            old_name='user_id',
            new_name='dba_user_id',
        ),
    ]
