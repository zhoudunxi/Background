# -*- coding: utf-8 -*-
#django http模块
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
#解决编码问题，返回中文,对上下文内容进行重用
from django.template import RequestContext
#导入‘数据库读取导航列表’模块
#from release.obtain_nav import header_left_nav
from setting.auth_permission_nav import AUTH_Perm
#导入表单模块,release的表单
from release.forms import Release_Form
from release.forms import DBA_Release_Form
#导入‘数据库’models模型模块,项目表
from project_manegement.models import project
from release.models import release, dba_release, dev_release, ops_release
#from setting.models import user_with_project
#时间
import time
#流程处理模块
from release.deal_process import untreated, BACKUPCOPY, UPDATECODE, ROLBACK, BACKCODE
from release.deal_process import releasetable, dba_releasetable, ops_releasetable, dev_releasetable, ops_toback
from release.deal_sendmail import send_to_dba, send_to_dev, send_to_ops
#django 将model转换为字典
from django.forms.models import model_to_dict
#css处理模块
from release.css_control import css_control
from release.deal_release_status import css_release_status #获取发布状态
#配置文件模块
import ConfigParser
#导入django 认证模块
from django.contrib import auth
#导入django的模型User表，因为认证用的是django的
from django.contrib.auth.models import User
# 导入django session模型，用于取出userid 
from django.contrib.sessions.models import Session
from setting.getprojectname import GetProjectName #获取项目名称

#流程中的权限控制
from release.deal_auth_permission import permission_control
#是否开启预发布
from release.deal_auth_permission import get_pre_env


#代码提交
@csrf_protect
#@permission_required(('release.change_release','release.change_activity_release'),login_url='/login/')
@login_required(login_url='/login/')
def Release(request):
	# 获取表单
	release_form = Release_Form()
	auth_return = AUTH_Perm(request, '代码提交')
	user_db = User.objects.get(id=auth_return[1])
	if user_db.is_staff or user_db.has_perm('release.change_release') or user_db.has_perm('release.change_activity_release'): 
		is_staff = auth_return[2]
		#隐藏报错div
		release_description_e = 'hidden'
		release_filelist_e = 'hidden'
		release_putsql_e = 'hidden'
		#报错处理
		error_re = request.GET.get('error')	
		if error_re == "projectnotchoose":
			error_re = '请选择项目'
		#从数据库中获取项目名
		if is_staff:
			project_name = project.objects.all().values_list('project_name')
		else:
			project_name = GetProjectName(auth_return[1])

		return render(request,'release.html',{'left_nav':auth_return[0],
			'release_form':release_form,
			'dba_release_form':DBA_Release_Form(),
			'release_description_e':release_description_e,
			'release_filelist_e':release_filelist_e,
			'release_putsql_e': release_putsql_e,
			'project_name':project_name,
			'error_re':error_re})
	else:
		return HttpResponseNotFound('<h1>ERROR: 少年！你没有权限！</h1>')
		

@csrf_protect
#@permission_required('release.change_release',login_url='/login/')
@login_required(login_url='/login/')
def Request(request):
	auth_return = AUTH_Perm(request, '代码提交') #返回，左导航，当前用户id，是否有管理员权限
	#从服务器里获取用户信息发布状态
	#release_status = project.objects.filter(id=0)
    # 如果是用POST提交来的表单
	if request.method == 'POST':
		#将表单里的数据写入变量
		release_form = Release_Form(request.POST)
		dba_release_form = DBA_Release_Form(request.POST)
		#用request.POST.getlist方法获取同一个name多个valu,这里传过来的是服务器的s_id
		#server_to_list = request.POST.getlist('server_t')
		project_name = request.POST.get('project_name') #源数据来自用户选择
		#developer_name = request.POST.get('developer_name') #源数据来自用户选择
		#user_id = request.POST.get('user_id') #一个隐藏的input，用户登陆的id，发布的操作者，来自auth_user表
		user_id = auth_return[1]
		doing = request.POST.get('doing') #获取post的doing，源数据来自页面
		putsql = request.POST.get('putsql') #获取页面的putsql，用户是否提交sql
		RequestID = request.POST.get('RequestID') #获取post的请求ID，源数据来自数据库release表
		if RequestID:
			release_status = release.objects.get(id=RequestID).release_status
		else:
			release_status = ''
                #判读表单是否为空或者说是否合法
		if not doing and not release_status:
			if permission_control(doing,user_id): #满足权限后才能进行以下操作
				if release_form.is_valid() and dba_release_form.is_valid():
					#developer_name = User.objects.get(id=user_id).last_name
					release_data = release_form.cleaned_data
					if project_name == "notChoose": #如果用户没有选择项目带报错返回
						return HttpResponseRedirect('/release/?error=projectnotchoose')
					release_data['project_id'] = project.objects.get(project_name=project_name).id
					release_data['description'] = release_data['description'] #去掉多系统换行
					release_data['filelist'] = release_data['filelist'].strip('\r\n') #去掉多系统换行
					release_data['begin_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # 获取当前系统时间
					release_data['release_status'] = '未处理'
					release_data['developer_name'] = User.objects.get(id=user_id).last_name
					release_data['last_user_id'] = user_id
					if putsql == 'have':
						release_data['is_have_sql'] = 1
					else:
						release_data['is_have_sql'] = 0
					release_to_db = release(**release_data) #写入到release表，上线主表
					release_to_db.save()
					request_ID = release.objects.filter(last_user_id=user_id).order_by('-id')
					request_ID = request_ID.values_list('id')[0][0]

					dev_add_db = dev_release(request_id=request_ID, dev_user_id=user_id) #写入到dev_release表开发状态表
					dev_add_db.save()
					ops_add_db = ops_release(request_id=request_ID) #写入ops表
					ops_add_db.save()
					if putsql == 'have':
						dba_release_data = dba_release_form.cleaned_data
						dba_release_data['sql_statement'] = dba_release_data['sql_statement'] #处理sql语句
						dba_release_data['request_id'] = request_ID
						dba_release_data['sql_action_status'] = 0
						sql_to_db = dba_release(**dba_release_data) #写入到dba——release, dba状态表，也记录sql
						sql_to_db.save()

						if get_pre_env(request_ID): #如果分支是master，就发送邮件，意思是线上才发邮件
							send_to_dba(request_ID)#发送邮件给dba
					else:
						nextpare = 'prepare'
						sql_to_db = dba_release(request_id=request_ID)  # 写入到dba——release, dba状态表，也记录sql
						sql_to_db.save()
						if get_pre_env(request_ID):
							send_to_ops(request_ID,putsql,nextpare)#发送邮件给运维
					back_copy = BACKUPCOPY(request_ID,ENV='init') #执行备份和复制
					if back_copy != 'success':
						update_data = release.objects.get(id=request_ID)
						update_data.release_status = 'GIT或备份失败'
						update_data.save()
					return HttpResponseRedirect('/release/request/?requestid=%s' % request_ID)
				else:
					#django 视图中用 下列方式获取报错，模板中是这样的add_s_group.group_name.errors
					if release_form['description'].errors:
						release_description_e = 'show'
					else:
						release_description_e = 'hidden'
					if release_form['putsql'].errors:
						release_putsql_e = 'show'
					else:
						release_putsql_e = 'hidden'
					if release_form['filelist'].errors:
						release_filelist_e = 'show'
					else:
						release_filelist_e = 'hidden'
					return render(request,'release.html',{'left_nav':auth_return[0],
														  'release_form':release_form,
														  'dba_release_form':dba_release_form,
														  'release_description_e':release_description_e,
														  'release_putsql_e':release_putsql_e,
														  'release_filelist_e':release_filelist_e,})
			else:
				return HttpResponseNotFound('<h1>ERROR: 少年！你没有权限！</h1>')
		#elif doing == 'prepare' and release_status.encode('utf-8') == '未处理': #满足发预发布条件
		elif doing == 'carry_sql': #dba执行完sql
			if permission_control(doing, user_id):  # 满足权限后才能进行以下操作
				releasetable(RequestID, '已执行SQL', user_id)
				dba_releasetable(RequestID,user_id) #dba操作后写入数据库
				putsql = 'have'
				nextpare = 'prepare'
				if get_pre_env(RequestID):
					send_to_ops(RequestID, putsql, nextpare)  # 发送邮件给运维
				return HttpResponseRedirect('/release/request/?requestid=%s' % RequestID)
			else:
				return HttpResponseNotFound('<h1>ERROR: 少年！你没有权限！</h1>')
		elif doing == 'prepare': #满足发预发布条件
			if permission_control(doing, user_id):  # 满足权限后才能进行以下操作
				uploads_status = UPDATECODE(RequestID) #执行发布
				if uploads_status == 'success':
					releasetable(RequestID,'已预发布',user_id)
				else:
					releasetable(RequestID,'预发布失败',user_id)
				ops_releasetable(RequestID,user_id,doing) #运维操作后写入数据库
				if get_pre_env(RequestID):
					send_to_dev(RequestID,doing,uploads_status) #发送邮件给开发
				return HttpResponseRedirect('/release/request/?requestid=%s&%s' %(RequestID,uploads_status))
			else:
				return HttpResponseNotFound('<h1>ERROR: 少年！你没有权限！</h1>')
		elif doing == 'dev_tested': #开发测试通过
			if permission_control(doing, user_id):  # 满足权限后才能进行以下操作
				releasetable(RequestID, '开发已测试', user_id)
				dev_releasetable(RequestID,user_id)
				putsql = 'buxuyao'
				nextpare = 'online'
				if get_pre_env(RequestID):
					send_to_ops(RequestID, putsql, nextpare)  # 发送邮件给运维
				return HttpResponseRedirect('/release/request/?requestid=%s' % RequestID)
			else:
				return HttpResponseNotFound('<h1>ERROR: 少年！你没有权限！</h1>')
		#elif doing == 'online' and release_status.encode('utf-8') == '已预发布': #满足发正式条件
		elif doing == 'online': #满足发正式条件
			if permission_control(doing, user_id):  # 满足权限后才能进行以下操作
				uploads_status = UPDATECODE(RequestID) #执行发布
				if uploads_status == 'success':
					releasetable(RequestID,'已发布',user_id)
				else:
					releasetable(RequestID,'发布失败',user_id)
				ops_releasetable(RequestID,user_id,doing)
				if get_pre_env(RequestID):
					send_to_dev(RequestID,doing,uploads_status)#  # 发送邮件给开发
				return HttpResponseRedirect('/release/request/?requestid=%s&%s' %(RequestID,uploads_status))
			else:
				return HttpResponseNotFound('<h1>ERROR: 少年！你没有权限！</h1>')
		elif doing == 'toback': #满足回滚条件
			if permission_control(doing, user_id):  # 满足权限后才能进行以下操作
				uploads_status = BACKCODE(RequestID) #执行回滚
				if uploads_status == 'success':
					releasetable(RequestID,'已回滚',user_id)
				else:
					releasetable(RequestID,'回滚失败',user_id)
				ops_toback(RequestID, user_id)
				if get_pre_env(RequestID):
					send_to_dev(RequestID,doing,uploads_status)  # 发送邮件给开发
				return HttpResponseRedirect('/release/request/?requestid=%s&%s' %(RequestID,uploads_status))
			else:
				return HttpResponseNotFound('<h1>ERROR: 少年！你没有权限！</h1>')
		
	else:
		RequestID = request.GET.get('requestid') #传统的get方法，url http://8.8.8.91/release/request/?requestid=10 获取value
		untreated_data = untreated(RequestID)
		try:
			enable_pre_env = untreated_data[1].enable_pre_env.encode('utf-8') #是否开启预发布，true是开启,测试环境是false	
		except:
			enable_pre_env = True
		release_data = model_to_dict(untreated_data[0])#调用流程模块，将描述和文件列表数据格式处理后返回给前端,model_to_dict转换成字典,这里获取到release表数据
		#release_data['user_name'] = user_name #将用户名放入字典中，返回给前端
		release_data['last_name'] = User.objects.get(id=release_data['last_user_id']).last_name #将用户名放入字典中，返回给前端
		try:
			release_data['project_name'] = project.objects.get(id=release_data['project_id']).project_name #项目名，返回给前端
		except:
			release_data['project_name'] = '该项目已经被删除'
		if release_data['is_have_sql']: #如果开发提交了sql
			release_data['sql_statement'] = untreated_data[2].sql_statement #需要上线的sql
		release_data['ops_user_list'] = untreated_data[3] #项目运维
		css_data = css_control(release_data,enable_pre_env,release_data['is_have_sql'],auth_return[1]) #调用css模块，控制上线按钮
		css_re_status = css_release_status(release_data,RequestID) #获取各个阶段的状态
		return render(request,'release_request.html',{'left_nav':auth_return[0],
													  'release_data':release_data,
													  'css_data':css_data,
													  'css_re_status':css_re_status})
