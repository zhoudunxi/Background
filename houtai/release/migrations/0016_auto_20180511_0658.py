# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-11 06:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0015_activity_release'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity_release',
            old_name='request_id',
            new_name='request_id1',
        ),
    ]
