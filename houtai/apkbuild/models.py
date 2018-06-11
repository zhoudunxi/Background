# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
#apk 更新逻辑队列表，每提交一次为一个队列
class apk_build_queue(models.Model):
	user_id = models.IntegerField() #用户id
	project_name = models.CharField(max_length=255) #项目名称-代号
	apk_version = models.CharField(max_length=120) #apk包的版本号
	message_total = models.IntegerField() #提交的渠道标识总数
	submit_time = models.DateTimeField(null=True,blank=True) #提交时间

#每个渠道apk制作详细表
class apk_message_detail(models.Model):
	build_queue_id = models.IntegerField() #队列ID
	channel_identification = models.CharField(max_length=255) #渠道标识
	work_ip = models.CharField(max_length=15,null=True,blank=True) #被work消费的ip地址
	build_start = models.BooleanField() #消费状态，开始消费，布尔类型1代表TRUE,0代表FALSE
	apk_build_status = models.BooleanField() #消费状态，apk制作完成
	cdn_renew_status = models.BooleanField() #消费状态, 刷新CDN完成
	all_done = models.BooleanField() #消费状态，校验文件和cdn状态，标志整个更新完成 
	begin_time = models.DateTimeField(null=True,blank=True) #work开始消费时间
	done_time  = models.DateTimeField(null=True,blank=True) #work结束消费时间
