# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-04-23 07:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ops_with_project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('project_id', models.IntegerField()),
            ],
        ),
    ]