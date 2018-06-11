# -*- coding: utf-8 -*-
#django http模块
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
#解决编码问题，返回中文,对上下文内容进行重用
from django.template import RequestContext
#导入‘数据库读取导航列表’模块
#from release.obtain_nav import header_left_nav
#导入‘认证权限和导航’模块
from setting.auth_permission_nav import AUTH_Perm
#导入表单
from setting.forms import User_Form
from setting.forms import user_return
#导入模型，用户表，项目表,用户项目关系表,权限控制表
#from django.contrib.auth.models import User
from  project_manegement.models import project
from setting.models import user_with_project
from django.contrib.auth.models import Permission
# 导入django session模型，用于取出userid 
from django.contrib.sessions.models import Session
from django.forms.models import model_to_dict ##django 将model转换为字典
from setting.getprojectname import GetProjectName #获取有权限的项目名称
from setting.getprojectname import AllProjectName #获取所有项目名称
#导入django的模型User表，因为认证用的是django的
from django.contrib.auth.models import User
from django.contrib import auth
import datetime
from setting.user_edit_password import user_edit_pwd #修改用户密码，写入到数据库
#from permission_create import UpdateAPKPers #调用django的认证机制，创建can_apkbuild权限
import edit_permissions #编辑权限模块
from setting.models import ops_duty #值班模型

@csrf_protect
@login_required(login_url='/login/')
def Setting(request):
	#if not request.user.is_authenticated(): #校验是否认证，如果没有认证跳转到登陆页面
	#	return HttpResponseRedirect('/login/?next=%s' % request.path)
	#session_key = request.session.session_key #获取sessionid
	#userid = Session.objects.get(pk=session_key).get_decoded()['_auth_user_id'] #更加sessionid查找出userid，根据userid做权限控制
	#left_return = header_left_nav('设置',userid) #调用模块，获取返回左导航元组数据
	auth_return = AUTH_Perm(request,'设置')
	userid = auth_return[1]
	#获取用户id，用户权限控制
	#is_staff = User.objects.get(id=userid).is_staff #用户身份
	is_staff = auth_return[2]
	if not is_staff:#非管理员用户跳转到404
		return HttpResponseNotFound('<h1>ERROR:404 少年！没事不要乱输入url！</h1>')

	if request.method == 'GET': #如果有get数据，就执行数据操作，这里是删除用户
		get_userid = request.GET.get('deleteuserid')
		if get_userid and get_userid != 1:
			user_dbdata = User.objects.get(id=get_userid)
			if user_dbdata.has_perm('release.change_ops_release'):  # 如果原来是运维，需要移除值班和管理的项目
				delete_duty = ops_duty.objects.filter(user_id=get_userid)
				delete_duty.delete()
				delete_project = user_with_project.objects.filter(user_id=get_userid)
                                delete_project.delete()
			if user_dbdata.has_perm('release.change_release'):
				delete_project = user_with_project.objects.filter(user_id=get_userid) #删除开发管理的项目
				delete_project.delete()
			User.objects.filter(id=get_userid).delete()
	user_from_db = User.objects.all()
	user_data = [] #需要前端展示的数据
	for user_list in user_from_db:
		if user_list.id == 1: #排除root用户，root用户不展示
			continue
		if user_list.is_staff:
			user_list.is_staff = '管理员'
		else:
			if user_list.has_perm('release.change_release'):
				user_list.is_staff = '开发'
			#if user_list.has_perm('apkbuild.can_apkbuild'):
			if user_list.has_perm('apkbuild.change_apk_build_queue'):
				user_list.is_staff = 'apk更新用户'
			if user_list.has_perm('release.change_dba_release'):
				user_list.is_staff = 'DBA用户'
			if user_list.has_perm('release.change_ops_release'):
				user_list.is_staff = '运维'
			if user_list.has_perm('release.change_activity_release'):
				user_list.is_staff = '活动开发'
		if user_list.date_joined == None:
			user_list.date_joined = '---'
		else:
			#print user_list.date_joined
			joined_CSTtime = user_list.date_joined + datetime.timedelta(hours=+8) #转换成东八区时间
			user_list.date_joined = joined_CSTtime.strftime('%Y-%m-%d %H:%M:%S')#转换时间格式
		if user_list.last_login == None:
			user_list.last_login = '---'
		else:
			login_CSTtime = user_list.last_login + datetime.timedelta(hours=+8)
			user_list.last_login = login_CSTtime.strftime('%Y-%m-%d %H:%M:%S')

		user_list = model_to_dict(user_list)#将数据转换成字典
		if user_list['is_staff'] == '管理员': #如果是管理员
			user_list['project_name'] = [('管理所有项目','')]
		elif user_list['is_staff'] == '开发':
			user_list['project_name'] = GetProjectName(user_list['id']) #获取项目名称
		elif user_list['is_staff'] == '运维':
			user_list['project_name'] = GetProjectName(user_list['id']) #获取项目名称
		elif user_list['is_staff'] == '活动开发':
			user_list['project_name'] = GetProjectName(user_list['id'])  # 获取项目名称
		else:
			user_list['project_name'] = [('---', '')]
		if user_list['is_staff'] == '运维':
			user_list['duty'] = True
			try:
				duty_status = ops_duty.objects.get(user_id=user_list['id']).duty_status
			except:
				duty_status = False
			if duty_status:
				user_list['duty_css'] = 'btn btn-sm btn-success btn-primary'
			else:
				user_list['duty_css'] = 'btn btn-sm btn-secondary-outline'
		user_data.append(user_list)

	return_data = {
		'left_nav': auth_return[0],
		'user_data': user_data}
	return render(request,'setting.html',return_data)

@csrf_protect
@login_required(login_url='/login/')
def ADD_User(request):
	auth_return = AUTH_Perm(request, '设置')
	left_return = auth_return[0]
	if not auth_return[2]:#非管理员用户跳转到404
		 return HttpResponseNotFound('<h1>ERROR:404 少年！没事不要乱输入url！</h1>') 
	user_form = User_Form() #获取表单
	 # 如果是用POST提交来的表单
	return_data = {
		'left_nav':auth_return[0],
		'user_form': User_Form()}
	if request.method == 'POST':
		#将表单里的数据写入变量
		user_form = User_Form(request.POST)
		projectid_list = request.POST.getlist('project_id') ##用request.POST.getlist方法获取同一个name多个valu,这里传过来的是项目ID
		if user_form.is_valid():
			user_data = user_form.cleaned_data#清理成Unicode对象,一个字典
			password = user_data['password']
			trypassword = user_data['trypassword']
			if password == trypassword:
				#将用户数据写入数据库
				username = user_data['username'].encode('utf-8')
				last_name = user_data['last_name'].encode('utf-8')
				email = user_data['email'].encode('utf-8')
				staff = user_data['is_staff'] #用户权限，true是管理员，false是普通用户
				user_to_db = User.objects.create_user(username=username,last_name=last_name,email=email,password=password)
				if staff == 'True':
					user_to_db.is_staff = True #必须要这样做
				user_to_db.save()
				user = User.objects.get(username=username)
				if staff == 'User' or staff == 'True': #如果是普通用户或者管理员用户身份，赋权
					change_release = Permission.objects.get(codename='change_release')
					user.user_permissions.add(change_release)

					for pro_ID in projectid_list: #将用户id和项目id写入表
						add_user_pro = user_with_project(user_id=user.id,project_id=pro_ID)
						add_user_pro.save()
				if staff == 'APKuser' or staff == 'True': #如果是apkuser或者管理员用户身份
					#赋予apk更新用户权限，普通用户与管理员以外的用户
					#can_apkbuild = Permission.objects.filter(codename='can_apkbuild') #从数据库查找can_apkbuild权限,必须用filter，如果权限不存
					change_apk_build_queue = Permission.objects.get(codename='change_apk_build_queue')
					user.user_permissions.add(change_apk_build_queue)  # 赋权 调用-->user.has_perm('apkbuild.can_apkbuild')
					#can_apkbuild = '(%S|%s|%S)' %(can_apkbuild)
					#if not can_apkbuild:
						#can_apkbuild = UpdateAPKPers()
					#else:
						#can_apkbuild = can_apkbuild[0]
					#user.user_permissions.add(can_apkbuild) #赋权 调用-->user.has_perm('apkbuild.can_apkbuild')
				if staff == 'DBAuser' or staff == 'True':
					change_release = Permission.objects.get(codename='change_dba_release')
					user.user_permissions.add(change_release)
				if staff == 'Opsuser' or staff == 'True':
					change_release = Permission.objects.get(codename='change_ops_release')
					user.user_permissions.add(change_release)
					add_duty = ops_duty(user_id=user.id,duty_status=False) #运维值班 表,现在叫请假表
					add_duty.save()
					for pro_ID in projectid_list: #将用户id和项目id写入表，用于接收邮件
						add_user_pro = user_with_project(user_id=user.id,project_id=pro_ID)
						add_user_pro.save()
				if staff == 'Activityuser' or staff == 'True': #如果是活动开发或者管理员用户身份，赋权
					change_release = Permission.objects.get(codename='change_activity_release')
					user.user_permissions.add(change_release)

					for pro_ID in projectid_list: #将用户id和项目id写入表
						add_user_pro = user_with_project(user_id=user.id,project_id=pro_ID)
						add_user_pro.save()

				return_data['add_status'] = 'success'
				return render(request,'setting_adduser.html',return_data)
			else:
				return_data['add_status'] = 'passwdERROE'
				return render(request,'setting_adduser.html',return_data)
	else:
		return_data['project_data'] = project.objects.all()
        return render(request,'setting_adduser.html',return_data)

@csrf_protect
@login_required(login_url='/login/')
def EDIT_User(request):
	auth_return = AUTH_Perm(request, '设置')
	if not auth_return[2]:#非管理员用户跳转404
		 return HttpResponseNotFound('<h1>ERROR:404 少年！没事不要乱输入url！</h1>')
	return_data = {
		'left_nav': auth_return[0]}
	if request.method == 'GET':
		edituserid = request.GET.get('edituserid')
		return_data['edituserid'] = edituserid
		user_dbdata = User.objects.get(id=edituserid)
		form_value = {'username': user_dbdata.username,
			'last_name': user_dbdata.last_name,
			'email': user_dbdata.email,}

		#用户身份对应关系
		identity = ''
		if user_dbdata.is_staff: #管理员
			identity = user_return('Admin')  # 权限对应关系
		else:
			if user_dbdata.has_perm('release.change_release'): #发布更新用户
				identity = user_return('User')
			if user_dbdata.has_perm('apkbuild.change_apk_build_queue'): #apk更新用户
				identity = user_return('APKuser')
			if user_dbdata.has_perm('release.change_dba_release'): #dba
				identity = user_return('DBAuser')
			if user_dbdata.has_perm('release.change_ops_release'): #运维
				identity = user_return('Opsuser')

		form_value['option_identity'] = identity
		if user_dbdata.has_perm('release.change_activity_release'):  # 活动用户，特殊处理
			form_value['option_identity'] = [('Activityuser', '活动开发')]
		#获取项目
		selected_objects = GetProjectName(edituserid)
		all_objects = AllProjectName()
		form_value['selected_objects'] = selected_objects
		form_value['unselected_objects'] = list(set(all_objects)-set(selected_objects))
		# user_form = EditUser_Form(
		# 	#initial 是修改表单里的初始值
		# 	initial={
		# 		'username':user_dbdata.username,
		# 		'last_name':user_dbdata.last_name,})
		return_data['form_value'] = form_value
		return render(request,'setting_edituser.html',return_data)
	else:
		if request.method == 'POST':
			edituserid = request.POST.get('edituserid')
			username = request.POST.get('username').encode('utf-8') #用户名
			last_name = request.POST.get('last_name').encode('utf-8') #中文名
			email = request.POST.get('email').encode('utf-8')
			staff = request.POST.get('is_staff') #权限
			projectid_list = request.POST.getlist('project_id') #项目列表
			user_dbdata = User.objects.get(id=edituserid)
			if username != user_dbdata.username:
				user_dbdata.username = username
			if last_name != user_dbdata.last_name:
				user_dbdata.last_name = last_name
			if email != user_dbdata.email:
				user_dbdata.email = email
			user_dbdata.save()
			#change_release = Permission.objects.get(codename='change_release')
			#change_apk_build_queue = Permission.objects.get(codename='change_apk_build_queue')
			if user_dbdata.is_staff and staff != 'True': #对管理员的权限操作，管理变成普通用户
				user_dbdata.is_staff = False
				if staff == 'User':
					edit_permissions.user_up_to_user('release.change_release', edituserid)  #移除老权限，只保留一个
				if staff == 'APKuser':
					edit_permissions.user_up_to_user('apkbuild.change_apk_build_queue', edituserid)
				if staff == 'DBAuser':
					edit_permissions.user_up_to_user('release.change_dba_release', edituserid)
				if staff == 'Opsuser':
					edit_permissions.user_up_to_user('release.change_ops_release', edituserid)
					add_duty = ops_duty(user_id=edituserid, duty_status=False)  # 运维值班 表
					add_duty.save()

			else: #对普通用户修改的权限操作
				if user_dbdata.has_perm('release.change_release') and staff == 'True':#如果是开发提升到管理员
					edit_permissions.user_up_to_admin('release.change_release',edituserid)#赋权
				if user_dbdata.has_perm('apkbuild.change_apk_build_queue') and staff == 'True':
					edit_permissions.user_up_to_admin('apkbuild.change_apk_build_queue', edituserid)
				if user_dbdata.has_perm('release.change_dba_release') and staff == 'True':
					edit_permissions.user_up_to_admin('release.change_dba_release', edituserid)
				if user_dbdata.has_perm('release.change_ops_release') and staff == 'True':
					edit_permissions.user_up_to_admin('release.change_ops_release', edituserid)
					delete_duty = ops_duty.objects.filter(user_id=edituserid)
					delete_duty.delete()

				if staff == 'User' and not user_dbdata.has_perm('release.change_release'):#普通用户修改成开发
					edit_permissions.user_up_to_user('release.change_release', edituserid)#移除老权限
					if user_dbdata.has_perm('release.change_ops_release'):#如果原来是运维，需要移除值班，项目
						delete_duty = ops_duty.objects.filter(user_id=edituserid)
						delete_duty.delete()
						edit_permissions.user_delete_project(edituserid)
				if staff == 'APKuser' and not user_dbdata.has_perm('apkbuild.change_apk_build_queue'):#普通用户修改成apk用户
					edit_permissions.user_up_to_user('apkbuild.change_apk_build_queue', edituserid)
					if user_dbdata.has_perm('release.change_release'):#如果是开发，需要删除项目
						edit_permissions.user_delete_project(edituserid)
					if user_dbdata.has_perm('release.change_ops_release'):#如果原来是运维，需要移除值班和项目
						delete_duty = ops_duty.objects.filter(user_id=edituserid)
						delete_duty.delete()
						edit_permissions.user_delete_project(edituserid)
				if staff == 'DBAuser' and not user_dbdata.has_perm('release.change_dba_release'):#修改成DBA
					edit_permissions.user_up_to_user('release.change_dba_release', edituserid)
					if user_dbdata.has_perm('release.change_release'):#如果是开发，需要删除项目
						edit_permissions.user_delete_project(edituserid)
					if user_dbdata.has_perm('release.change_ops_release'):  # 如果原来是运维，需要移除值班和项目
						delete_duty = ops_duty.objects.filter(user_id=edituserid)
						delete_duty.delete()
						edit_permissions.user_delete_project(edituserid)
				if staff == 'Opsuser' and not user_dbdata.has_perm('release.change_ops_release'):#修改成运维
					edit_permissions.user_up_to_user('release.change_ops_release', edituserid)
					if user_dbdata.has_perm('release.change_release'):#如果是开发，需要删除项目
						edit_permissions.user_delete_project(edituserid)
					add_duty = ops_duty(user_id=edituserid, duty_status=False)  # 运维值班 表
					add_duty.save()

			if staff == 'True' or staff == 'User' or staff == 'Opsuser' or staff == 'Activityuser': #管理员、普通用户修改成开发或者运维后的项目修改
				#如果原来就是开发或者运维，只是修改项目
				if user_dbdata.has_perm('release.change_release') or user_dbdata.has_perm('release.change_ops_release') or user_dbdata.has_perm('release.change_activity_release'):
					from_db_projectid = user_with_project.objects.filter(user_id=edituserid).values_list('project_id')
					db_projectid_list = []
					for db_pro in from_db_projectid:
						db_projectid_list.append(unicode(db_pro[0]))
					add_projectid = list(set(projectid_list) - set(db_projectid_list))
					del_projectid = list(set(db_projectid_list) - set(projectid_list))
					if add_projectid:
						for pro_ID in add_projectid:
							try:
								get_u_p = user_with_project.objects.get(user_id=edituserid, project_id=pro_ID)
							except:
								add_user_pro = user_with_project(user_id=edituserid, project_id=pro_ID)
								add_user_pro.save()
					if del_projectid:
						for pro_ID in del_projectid:
							get_u_p = user_with_project.objects.get(user_id=edituserid, project_id=pro_ID)
							get_u_p.delete()
				#其他用户
				else:
					for pro_ID in projectid_list:  # 将用户id和项目id写入表
						add_user_pro = user_with_project(user_id=edituserid, project_id=pro_ID)
						add_user_pro.save()


			return_data['edit_status'] = 'success'
		return render(request,'setting_edituser.html',return_data)

@csrf_protect
@login_required(login_url='/login/')
def E_PWD_User(request):
	auth_return = AUTH_Perm(request, '设置')
	#if not auth_return[2]:  # 非管理员用户跳转404
		#return HttpResponseNotFound('<h1>ERROR:404 少年！没事不要乱输入url！</h1>')
	return_data = {
		'left_nav': auth_return[0]}
	if request.method == 'GET':
		return_data['edituserid'] = request.GET.get('edituserid')
		return_data['editstaff'] = User.objects.get(id=request.GET.get('edituserid')).is_staff
		return_data['last_name'] = User.objects.get(id=return_data['edituserid']).last_name
		return render(request,'setting_editpassword.html', return_data)
	else:
		if request.method == 'POST':
			edituserid = request.POST.get('edituserid')
			password = request.POST.get('password')
			trypassword = request.POST.get('trypassword')
			edit_user = User.objects.get(id=edituserid)
			#如果是普通用户自己修改密码，或者是管理员修改自己的密码，需要验证身份
			if not auth_return[2] or auth_return[2] == edit_user.is_staff:
				oldpassword = request.POST.get('oldpassword')
				userauth = auth.authenticate(username=edit_user.username,password=oldpassword)
				if userauth  is not None and userauth.is_active:
					return_data['edit_status'] = user_edit_pwd(edituserid,password,trypassword)
			else:
				return_data['edit_status'] = user_edit_pwd(edituserid,password, trypassword)
			return_data['edituserid'] = edituserid
		return render(request,'setting_editpassword.html', return_data)




