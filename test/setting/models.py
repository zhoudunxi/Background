# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
#用户与项目对应表,添加用户写入，用于针对用户赋权项目
class user_with_project(models.Model):
	user_id = models.IntegerField() #用户ID
	project_id = models.IntegerField() #项目ID

class ops_duty(models.Model): #以前用于值班，现在用于请假
	user_id =  models.IntegerField() #用户ID
	duty_status = models.BooleanField() #值班状态

#运维对应项目，用于运维可管理的项目，接收上线邮件
#class ops_with_project(models.Model): #
#	user_id = models.IntegerField()  # 用户ID
#	project_id = models.IntegerField()  # 项目ID