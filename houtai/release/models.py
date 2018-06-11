# -*- coding: utf-8 -*-
from django.db import models
from project_manegement.models import project

# Create your models here.
#左导航
class left_nav(models.Model):
	#自动增长唯一的列
        left_navid = models.AutoField(primary_key=True,unique=True)
	#上级目录id
        left_nav_pid = models.IntegerField()
	#标题
        left_nav_title = models.CharField(max_length=50)
	#a连接
        left_nav_url = models.CharField(max_length=240)
	#排序用的数字
        left_nav_sort = models.IntegerField()

	def __unicode__(self):
		return u'%s %s %s %s' % (self.left_nav_pid, self.left_nav_title, self.left_nav_url, self.left_nav_sort)

class release(models.Model):
	project_id = models.IntegerField() #项目ID
	#project_id = models.ForeignKey(project) #项目ID
	description = models.TextField(blank=True) #上线描述
	filelist =  models.TextField() #上线的文件列表
	release_status = models.CharField(max_length=50) #上线到的环境
	is_have_sql = models.BooleanField(default=0) #是否有sql
	#dev_user_id = models.IntegerField(null=True,blank=True) #用户id
	developer_name = models.CharField(max_length=30) #请求人的名字，开发者的名字
	last_user_id =  models.IntegerField(null=True,blank=True) #最后提交的用户id
	begin_time = models.DateTimeField(null=True,blank=True) #提交时间
	last_time = models.DateTimeField(null=True,blank=True) #最后提交时间

	def __unicode__(self):
               	return u'project_id:%s \ndescription:%s \nfilelist:%s \nrelease_status:%s \nlast_user_id:%s \nbegin_time:%s \nlast_time:%s \n \n' % ( self.project_id, self.description, self.filelist, self.release_status, self.last_user_id, self.begin_time, self.last_time)

class dba_release(models.Model):
	request_id = models.IntegerField(null=True, blank=True)  # 上线ID
	dba_user_id = models.IntegerField(null=True,blank=True) #处理sql提交的DBA用户
	sql_statement = models.TextField(blank=True) #开发提交的sql
	sql_action_status = models.BooleanField(default=0) #dba 执行sql的状态

class ops_release(models.Model):
	request_id = models.IntegerField() #上线ID
	pre_user_id = models.IntegerField(null=True,blank=True) #发布到预发布的运维用户
	ops_to_pre_status = models.BooleanField(default=0) #运维上线预发布
	online_user_id = models.IntegerField(null=True,blank=True)  #发布到正式的运维用户
	ops_to_online_status = models.BooleanField(default=0)  # 运维上线到正式
	toback_user_id = models.IntegerField(null=True, blank=True)  # 发布到正式的运维用户
	ops_toback_status = models.BooleanField(default=0)  # 运维上线到正式
	upload_file_status = models.TextField(blank=True) #上线文件状态，磊哥上传文件模块返回的状态

class dev_release(models.Model):
	request_id = models.IntegerField()  # 上线ID
	dev_user_id = models.IntegerField(null=True, blank=True)  # 开发用户id
	dev_to_online_status = models.BooleanField(default=0)  # 开发确认上线到正式

class activity_release(models.Model):
	request_id = models.IntegerField()  # 上线ID
