# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
#项目
class project(models.Model):
	project_name = models.CharField(max_length=500) #项目名称
	cmdb_group_id = models.IntegerField(null=True,blank=True) #cmdb中分组的id
	project_description = models.CharField(max_length=2048,blank=True) #项目描述
	project_label = models.CharField(max_length=500) #项目描述，用于sync脚本, 目前用于项目目录
	storage_id = models.IntegerField() #storage id
	remote_path = models.CharField(max_length=999,blank=True) #远程主机目录
	pre_remote_path = models.CharField(default='none',max_length=999,blank=True) #预发布远程主机目录
	def __unicode__(self):
		return u'%s %s %s %s' % ( self.project_name, self.project_description, self.project_label, self.storage_id)

#git仓库，备份，工作目录等
class storage(models.Model):
	name = models.CharField(max_length=500) #名称,不可重复
	description = models.CharField(max_length=2048,blank=True) #描述
	back_path = models.CharField(max_length=999) #备份文件存放区根目录
	git_path = models.CharField(max_length=999) #git仓库根目录
	staging_path = models.CharField(max_length=999) #镜像目录，暂存目录
#	sync_script = models.CharField(max_length=999) #同步脚本
	branch_name = models.CharField(max_length=10) #代码分支，master/test
	enable_pre_env = models.CharField(max_length=10) #是否启用预发布环境
	staging_path_for_pre = models.CharField(max_length=999,blank=True) #预发布镜像目录，暂存目录
#	sync_script_for_pre = models.CharField(max_length=999,blank=True) #预发布同步脚本
