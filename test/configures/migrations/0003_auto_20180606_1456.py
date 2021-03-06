# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-06-06 06:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configures', '0002_envdb_nginxdb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='envdb',
            name='env',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='envdb',
            name='envname',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='nginxdb',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='nginxdb',
            name='env',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='nginxdb',
            name='filename',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='nginxdb',
            name='lastcontent',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='nginxdb',
            name='modifytime',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='nginxdb',
            name='projectid',
            field=models.CharField(db_index=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='nginxdb',
            name='projectname',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='phpfpmdb',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='phpfpmdb',
            name='env',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='phpfpmdb',
            name='filename',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='phpfpmdb',
            name='lastcontent',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='phpfpmdb',
            name='modifytime',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='phpfpmdb',
            name='projectid',
            field=models.CharField(db_index=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='phpfpmdb',
            name='projectname',
            field=models.CharField(max_length=30),
        ),
    ]
