# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-04-03 03:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0002_auto_20180403_1139'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ops_release',
            old_name='ops_to_preonline_status',
            new_name='ops_to_pre_status',
        ),
    ]