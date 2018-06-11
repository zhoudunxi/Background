#coding=UTF-8

from __future__ import unicode_literals
from django.db import models
import time


class envdb(models.Model):
    #Environment id. 1000:'生产'；1001:'灰度'；1002：'预生产'；1003'测试'.
    env = models.IntegerField(db_index=True)
    envname = models.CharField(max_length=30)

class phpfpmdb(models.Model):
    #project id
    projectid = models.IntegerField(db_index=True) 
    #configure file name
    filename = models.CharField(max_length=30)
    #The last modify time
    modifytime = models.CharField(max_length=30)
    #data of the php-fpm configures file
    content = models.TextField()
    #Backup that data of the php-fpm configures file
    lastcontent = models.TextField(null=True)
    #Running environment.
    env = models.IntegerField()

class nginxdb(models.Model):
    #project id
    projectid = models.IntegerField(db_index=True) 
    #configure file name
    filename = models.CharField(max_length=30)
    #The last modify time
    modifytime = models.CharField(max_length=30)
    #data of the php-fpm configures file
    content = models.TextField()
    #Backup that data of the php-fpm configures file
    lastcontent = models.TextField(null=True)
    #Running environment.
    env = models.IntegerField()