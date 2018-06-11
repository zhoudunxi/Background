# -*- coding: utf-8 -*-
from __future__ import division
import json, time, datetime, json
#django http模块
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.http import HttpResponse, HttpResponseForbidden
#认证和左导航,这里调用apk渠道标识提交的视图的里的一个方法
#导入‘认证权限和导航’模块
from setting.auth_permission_nav import AUTH_Perm
# 导入django session模型，用于取出userid 
from apkbuild.models import apk_build_queue #apk逻辑队列表
from apkbuild.models import apk_message_detail #每个渠道apk制作详细表
from django.contrib.auth.models import User #django 认证用户表
from django.forms.models import model_to_dict ##django 将model转换为字典
#导入分页模块
from apkbuild.paging_for_apk import Paging

@csrf_protect
@permission_required('apkbuild.change_apk_build_queue',login_url='/login/')
def APKQueue_Detail(request):
	if not request.user.is_authenticated(): #校验是否认证，如果没有认证跳转到登陆页面
		return HttpResponseRedirect('/login/?next=%s' % request.path)
	auth_return = AUTH_Perm(request,'APK队列') #认证赋权-->返回 左导航 用户id 用户权限 是否管理员
	#if not auth_return[2]:#没有权限跳转到404
		#return HttpResponseNotFound('<h1>ERROR:404 少年！没事不要乱输入url！</h1>')
	
	# 处理数据
	build_queue_id = int(request.GET.get('queue_id'))
	current_page = 1 #默认当前页
	columns_table = 50 #表显示列数
	if request.GET.get('pages-id'):#如果get到url中指定的页码，设置当前页
		current_page=int(request.GET.get('pages-id'))
	select_total = ''
	queue_list = ''
	id_start = current_page * columns_table - columns_table
	id_end = id_start + columns_table
		
	select_total = apk_message_detail.objects.filter(build_queue_id=build_queue_id).count() #根据队列id查找数据
	queue_data = apk_message_detail.objects.filter(build_queue_id=build_queue_id).order_by('-id')[id_start:id_end]
	queue_list = Paging(current_page, columns_table, 5, select_total) #传参说明：当前页，表显示列数，分页显示数, 数据收录条数, 用户有权限查看的数据
	countI = 0
	display_data = []
	#queue_idstr = ''
	while countI < len(queue_data):
		data_from_db = model_to_dict(queue_data[countI])
		if data_from_db['begin_time'] != None:	
			data_from_db['begin_time'] = data_from_db['begin_time'].strftime('%Y-%m-%d %H:%M:%S')	
		else:
			data_from_db['begin_time'] = ''
		if data_from_db['done_time'] != None:
			data_from_db['done_time'] = data_from_db['done_time'].strftime('%Y-%m-%d %H:%M:%S')
		else:
			data_from_db['done_time'] = ''
		if not data_from_db['build_start']:
			detail_id = data_from_db['id']
			ch_identifly = data_from_db['channel_identification']
			data_from_db = {}
			data_from_db['id'] = detail_id
			data_from_db['channel_identification'] = ch_identifly
			data_from_db['build_start'] = '未开始' 
			display_data.append(data_from_db)
			countI += 1
			continue
		else:
			data_from_db['build_start'] = '已开始'
		if data_from_db['apk_build_status']:
			data_from_db['apk_build_status'] = '已处理'	 
		else:
			data_from_db['apk_build_status'] = ''
		if data_from_db['cdn_renew_status']:
			data_from_db['cdn_renew_status'] = '已处理'
		else:
			data_from_db['cdn_renew_status'] = ''
		if data_from_db['all_done']:
			data_from_db['all_done'] = '完成'
		else:
			data_from_db['all_done'] = ''
			
		#submit_CSTtime = queue_data[countI].submit_time + datetime.timedelta(hours=+8)
		#data_from_db['submit_time'] = submit_CSTtime.strftime('%Y-%m-%d %H:%M:%S') #转换成东八区时间
		
		display_data.append(data_from_db)
		#queue_idstr = queue_idstr + str(data_from_db['id']) + '|'
		countI += 1
		
	return render(request,'apkqueuedetail.html',{
		'left_nav':auth_return[0], 
		'current_page':current_page,
		'display_list':queue_list, 
		'display_data':display_data,
		'build_queue_id':build_queue_id,
		})

