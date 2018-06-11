# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.
class cmdbmanage(models.Model):
    uid = models.CharField(max_length=30) #机器id
    server_ip = models.CharField(max_length=30) #机器ip地址
    server_mem =  models.CharField(max_length=30) #机器内存u
    server_cpu = models.CharField(max_length=50) #机器cpu
    server_system = models.CharField(max_length=30) #机器系统类型
    server_position = models.CharField(max_length=30) #机器服务商
    server_service = models.CharField(max_length=30) #机器提供服务项
    group = models.CharField(max_length=300) #机器所属项目
    env = models.CharField(max_length=10) #机器所属环境


class cmdbgroup(models.Model):
    optionid = models.CharField(max_length=30)#option id
    progroup = models.CharField(max_length=30)#项目组
