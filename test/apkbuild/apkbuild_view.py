# -*- coding: utf-8 -*-
import json, time, os, sys, ConfigParser
#django http模块
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.http import HttpResponse, HttpResponseForbidden
#解决编码问题，返回中文,对上下文内容进行重用
from django.template import RequestContext
#导入‘数据库读取导航列表’模块
#from release.obtain_nav import header_left_nav
#导入django 认证模块
#from django.contrib import auth
#导入django的模型User表，因为认证用的是django的
from django.contrib.auth.models import User
# 导入django session模型，用于取出userid 
#from django.contrib.sessions.models import Session
#导入‘认证权限和导航’模块
from setting.auth_permission_nav import AUTH_Perm

from apkbuild.models import apk_build_queue #apk逻辑队列表
from apkbuild.models import apk_message_detail #每个渠道apk制作详细表

#apk 构建 ，更新cdn，发送邮件
#import apkbuild.BuildApk, os , sys, apkbuild.tests, multiprocessing
from apkbuild.production_rabbitmq import APK_Production
from apkbuild.check_remotefile import Check_File #校验远程文件模块
from apkbuild.get_project_config import Project_Info #从配置文件中获取项目信息

# @csrf_protect
# def AUTH_Perm(request,leftnav):#认证权限
# 	session_key = request.session.session_key #获取sessionid
# 	userid = Session.objects.get(pk=session_key).get_decoded()['_auth_user_id'] #更加sessionid查找出userid，根据userid做权限控制
# 	left_nav_db = header_left_nav(leftnav,userid) #调用模块，获取返回左导航元组数据
#
#
#         #获取用户id，用户权限控制
#         user_db = User.objects.get(id=userid)
#         is_staff = user_db.is_staff #用户身份
#         #change_release = user_db.has_perm('apkbuild.can_apkbuild') #用户权限
#         change_release = user_db.has_perm('apkbuild.change_apk_build_queue') #用户权限
#
# 	return (left_nav_db,userid,change_release,is_staff)

#代码提交表单
@csrf_protect
@permission_required('apkbuild.change_apk_build_queue',login_url='/login/')
def APKBuild(request):
	# if not request.user.is_authenticated(): #校验是否认证，如果没有认证跳转到登陆页面
	# 	return HttpResponseRedirect('/login/?next=%s' % request.path)
	# auth_return = AUTH_Perm(request,'更新APK') #认证赋权
	#if not auth_return[2]:#没有权限跳转到404
		#return HttpResponseNotFound('<h1>ERROR:404 少年！没事不要乱输入url！</h1>')
	auth_return = AUTH_Perm(request, '更新APK')
	print auth_return
	if auth_return[2]:#如果是管理员显示优先级
		priority_class = 'show'
	else:
		priority_class = 'hidden'
	project_info = Project_Info() #从配置文件中获取项目信息，包括项目项目代号列表，{中文名，项目版本号}

	return render(request,'apkbuild.html',{
	'left_nav':auth_return[0],
	'priority_class':priority_class,
	'project_info':project_info
	})

#apk post流程处理
@csrf_protect
@permission_required('apkbuild.change_apk_build_queue',login_url='/login/')
def APKRequest(request):
	# if not request.user.is_authenticated(): #校验是否认证，如果没有认证跳转到登陆页面
	# 	return HttpResponseRedirect('/login/?next=%s' % request.path)
     #    auth_return = AUTH_Perm(request,'更新APK') #认证赋权
     #    if not auth_return[2]:#没有权限跳转到404
     #             return HttpResponseNotFound('<h1>ERROR:404 少年！没事不要乱输入url！</h1>')
	auth_return = AUTH_Perm(request, '更新APK')  # 认证赋权
	username = User.objects.get(id=auth_return[1]).username
	if request.method == 'POST':
		project_name = request.POST.get('project_name')
		apkversion = request.POST.get('apkversion')
		identify = request.POST.get('identify')
		queue_priority = request.POST.get('queue_priority')
		version = apkversion.strip('\r\n').encode('utf-8')
		lists = identify.strip('\r\n').encode('utf-8').split() #去空格和回车，格式化成列表

		#校验apk文件是否存在
		apk_file = '%s-%s.apk' %(project_name, apkversion)
		apk_file_status = Check_File(apk_file)
		if int(apk_file_status) == 0:#如果文件不存在，状态返回给前端
			return HttpResponse(json.dumps({'result':1}))
			
		#优先级处理
		if auth_return[2]: #如果是管理员
			message_priority = int(queue_priority)
		else: #其他用户优先级为1
			message_priority = 1
		
		#Main = apkbuild.BuildApk.BuildApk(username, version, lists)
		#output = Main.run()
		
		#写入apk更新逻辑队列表，获取队列ID
		submit_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		build_queue_to_db = apk_build_queue(user_id=auth_return[1], 
				apk_version=version, message_total=len(lists), 
				submit_time=submit_time, project_name=project_name)
		build_queue_to_db.save()
		build_queue_id = apk_build_queue.objects.filter(user_id=auth_return[1]).order_by('-id')
		build_queue_id = build_queue_id.values_list('id')[0][0]
		
		message_detail_data = {}
		#每条渠道标识写入apk制作详细表
		message_detail_data['build_queue_id'] = build_queue_id
		#message_detail_data['work_ip'] = '255.255.255.255'
		message_detail_data['build_start'] =  False
		message_detail_data['apk_build_status'] = False
		message_detail_data['cdn_renew_status'] = False
		message_detail_data['all_done'] = False
		for LISTone in lists:
			message_detail_data['channel_identification'] = LISTone
			message_detail_to_db = apk_message_detail(**message_detail_data)
			message_detail_to_db.save() #写入数据库
			message_id = apk_message_detail.objects.filter(build_queue_id=build_queue_id).order_by('-id').values_list('id')[0][0]
			APK_Production(message_id, version, LISTone, message_priority, project_name) #写入消息队列rabbitmq，消息ID：版本号：渠道标识：优先级：项目名	
		output = 0
		return HttpResponse(json.dumps({'result':output}))
	else:
		return HttpResponse(json.dumps({'result':'error'}))

