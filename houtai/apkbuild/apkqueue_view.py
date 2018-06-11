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
#解决编码问题，返回中文,对上下文内容进行重用
from django.template import RequestContext
#认证和左导航,这里调用apk渠道标识提交的视图的里的一个方法
#from apkbuild.apkbuild_view import AUTH_Perm
from setting.auth_permission_nav import AUTH_Perm
# 导入django session模型，用于取出userid 
from apkbuild.models import apk_build_queue #apk逻辑队列表
from apkbuild.models import apk_message_detail #每个渠道apk制作详细表
from django.contrib.auth.models import User #django 认证用户表
from django.forms.models import model_to_dict ##django 将model转换为字典
from django.db.models import Q
#导入分页模块
from apkbuild.paging_for_apk import Paging
from apkbuild.get_project_config import Get_CN_Name #获取配置文件中的中文项目名称


def _Deal_data(select_total, queue_data):
	countI = 0
	display_data = []
	queue_idstr = ''
	while countI < len(queue_data):
		data_from_db = model_to_dict(queue_data[countI])
		try:
			data_from_db['last_name'] = User.objects.get(id=data_from_db['user_id']).last_name #用户名
		except:
			data_from_db['last_name'] = '用户被删'
		submit_CSTtime = queue_data[countI].submit_time + datetime.timedelta(hours=+8)
		data_from_db['submit_time'] = submit_CSTtime.strftime('%Y-%m-%d %H:%M:%S') #转换成东八区时间
		data_from_db['done_count'] = apk_message_detail.objects.filter(
			Q(build_queue_id=data_from_db['id']),
			Q(apk_build_status=1)).count() #制作完成，领导说的,这样看起来快快的。		
			#Q(all_done=1)).count() #处理成功数,来自队列详细表
		if data_from_db['project_name'].encode('utf-8'):
			data_from_db['project_name'] = Get_CN_Name(data_from_db['project_name'].encode('utf-8')) #将英文名（代号）转换成配置文件中的中文项目名称
		else:
			data_from_db['project_name'] = Get_CN_Name('sdjj') #将英文名（代号）转换成配置文件中的中文项目名称
		# 处理百分比
		try:
			data_from_db['percent'] = int(int(data_from_db['done_count'])/int(data_from_db['message_total'])*100) #处理成功数/总数*100	
		except ZeroDivisionError:
			data_from_db['percent'] = 100
		
		display_data.append(data_from_db)
		queue_idstr = queue_idstr + str(data_from_db['id']) + '|' #用于post获取进度
		countI += 1
	return (display_data, queue_idstr)

@csrf_protect
@permission_required('apkbuild.change_apk_build_queue',login_url='/login/')
def APKQueue(request):
	if not request.user.is_authenticated(): #校验是否认证，如果没有认证跳转到登陆页面
		return HttpResponseRedirect('/login/?next=%s' % request.path)
	auth_return = AUTH_Perm(request,'APK队列') #认证赋权-->返回 左导航 用户id 用户权限 是否管理员
	#if not auth_return[2]:#没有权限跳转到404
		#return HttpResponseNotFound('<h1>ERROR:404 少年！没事不要乱输入url！</h1>')
	
	#硬件信息表
	current_page = 1 #默认当前页
	columns_table = 10 #表显示列数
	if request.GET.get('pages-id'):#如果get到url中指定的页码，设置当前页
		current_page=int(request.GET.get('pages-id'))
	select_total = ''
	queue_list = ''
	id_start = current_page * columns_table - columns_table
	id_end = id_start + columns_table
	if auth_return[2] == True:  #如果是管理员显示全部
		select_total = apk_build_queue.objects.all().count()
		queue_data = apk_build_queue.objects.all().order_by('-id')[id_start:id_end]
		deal_return = _Deal_data(select_total, queue_data)
		display_data = deal_return[0]
		queue_idstr = deal_return[1]
		queue_list = Paging(current_page, columns_table, 5, select_total) #传参说明：当前页，表显示列数，分页显示数, 数据收录条数, 用户有权限查看的数据
		
	else:#普通用户显示自己提交的数据
		select_total = apk_build_queue.objects.filter(user_id=int(auth_return[1])).count()
		queue_data = apk_build_queue.objects.filter(user_id=int(auth_return[1])).order_by('-id')[id_start:id_end]
		deal_return = _Deal_data(select_total, queue_data)
		display_data = deal_return[0]
		queue_idstr = deal_return[1]
		queue_list = Paging(current_page, columns_table, 5, select_total) #传参说明：当前页，表显示列数，分页显示数, 数据收录条数, 用户有权限查看的数据
		
		
	return render(request,'apkqueue.html',{
		'left_nav':auth_return[0], 
		'current_page':current_page,
		'display_data':display_data,
		'display_list':queue_list, 
		'queue_idstr':queue_idstr,
		})


@csrf_protect
@permission_required('apkbuild.change_apk_build_queue',login_url='/login/')
def Status_Queue(request):
	if not request.user.is_authenticated(): #校验是否认证，如果没有认证跳转到登陆页面
		return HttpResponseRedirect('/login/?next=%s' % request.path)
	auth_return = AUTH_Perm(request,'APK队列') #认证赋权
	#if not auth_return[2]:#没有权限跳转到404
		#return HttpResponseNotFound('<h1>ERROR:404 少年！没事不要乱输入url！</h1>')
	
	if request.method == 'POST':
		queue_idstr = request.POST.get('queue_idstr').split('|')
		queue_idstr.pop()
		return_dit = {} #需要返回的字典
		for queue_id in queue_idstr:
			sing_dit = {}
			done_message = apk_message_detail.objects.filter(
					Q(build_queue_id=int(queue_id)),
					Q(apk_build_status=1)).count() #制作完成，领导说的，这样看起来快快的。		
					#Q(all_done=1)).count() #处理成功数,来自队列详细表		
			sing_dit['done_message'] = done_message
			total_messages = apk_build_queue.objects.get(id=int(queue_id)).message_total
			sing_dit['total_message'] = total_messages
			sing_dit['percent'] = int(int(done_message)/int(total_messages)*100)		
			return_dit[queue_id] = sing_dit 

		return HttpResponse(json.dumps(return_dit))
	#{"32":{'percent':'80','done_message':'80','total_message':'100'},
	#"33":{'percent':'10','done_message':'10','total_message':'1000'}}
		
