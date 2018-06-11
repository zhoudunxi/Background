# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-25 02:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0003_auto_20180509_1437'),
    ]

    operations = [
        migrations.CreateModel(
            name='cmdbgroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('optionid', models.CharField(max_length=30)),
                ('progroup', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='cmdbmanage',
            name='env',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cmdbmanage',
            name='group',
            field=models.CharField(max_length=30),
        ),
    ]