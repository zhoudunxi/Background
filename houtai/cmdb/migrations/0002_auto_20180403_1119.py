# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-04-03 03:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cmdbmanage',
            old_name='operation',
            new_name='server_position',
        ),
        migrations.RemoveField(
            model_name='cmdbmanage',
            name='order_id',
        ),
    ]