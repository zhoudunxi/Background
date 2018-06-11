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
from setting.auth_permission_nav import AUTH_Perm
#导入release模型
from release.models import release ,dba_release, dev_release, ops_release#发布表
from django.contrib.auth.models import User #用户认证表
from setting.models import user_with_project #用户ID与项目ID关系表
#导入分页模块
#from listrequest.userpaging import UserPaging
from public.paging import Paging
#处理数据库取出的数据，用于前端展示
from listrequest.deal_data import deal_display_data, or_select
# 导入django session模型，用于取出userid 
from django.contrib.sessions.models import Session
from django.db.models import Q #用于数据库or查询

@csrf_protect
@login_required(login_url='/login/')
def REList(request):
	auth_return = AUTH_Perm(request, '请求列表')
	is_staff = auth_return[2]

	current_page = 1 #默认当前页
	columns_table = 10  # 表显示列数
	pageing_nub = 5 #分页显示数
	if request.GET.get('pages-id'):#如果get到url中指定的页码，设置当前页
			current_page=int(request.GET.get('pages-id'))
	select_total = ''
	release_list = ''
	id_start = current_page * columns_table - columns_table
	id_end = id_start + columns_table
	if is_staff: #如果是管理员
		release_data = release.objects.all().order_by('-id')[id_start:id_end]
		display_data = deal_display_data(release_data)
		select_total = release.objects.all().count()
		release_list = Paging(current_page, columns_table, pageing_nub, select_total)  # 传参说明：当前页，表显示列数，分页显示数, 数据收录条数

	else:
		user_from_db = User.objects.get(id=auth_return[1])
		#如果有开发权限根据开发上线表查询
		if user_from_db.has_perm('release.change_release') or user_from_db.has_perm('release.change_activity_release'):
			# 获取开发上线表，只获取当前开发用户的数据
			dev_data = list(dev_release.objects.filter(dev_user_id=user_from_db.id).order_by('-id')[id_start:id_end].values_list('request_id'))
			#字符拼接成Q或查询,
			orselect = or_select('id',dev_data) #说明： 字段名（这里是release表中的上线id），列表
			#执行或查询
			if orselect == 0:
				release_data = []
			else:
				release_data = release.objects.filter(orselect).order_by('-id')
			#处理数据库读出来的数据
			display_data = deal_display_data(release_data)
			select_total = dev_release.objects.filter(dev_user_id=user_from_db.id).count()
			release_list = Paging(current_page,
								  columns_table,
								  pageing_nub,
								  select_total)  # 传参说明：当前页，表显示列数，分页显示数, 数据收录条数

		#如果有dba权限，根据dba上线表查询
		elif user_from_db.has_perm('release.change_dba_release'):
			# 获取dba上线表，只获取当前开发用户的数据
			#dev_data = list(dba_release.objects.filter(dba_user_id=user_from_db.id).order_by('-id')[id_start:id_end].values_list('request_id'))
			dev_data = list(dba_release.objects.all().order_by('-id')[id_start:id_end].values_list('request_id'))
			# 字符拼接成Q或查询,
			orselect = or_select('id', dev_data)  # 说明（这里是release表中的上线id）： 字段名，列表
			# 执行或查询
			if orselect == 0:
				release_data = []
			else:
				release_data = release.objects.filter(orselect).order_by('-id')
			# 处理数据库读出来的数据
			display_data = deal_display_data(release_data)
			select_total = dba_release.objects.filter(dba_user_id=user_from_db.id).count()
			release_list = Paging(current_page,
								  columns_table,
								  pageing_nub,
								  select_total)  # 传参说明：当前页，表显示列数，分页显示数, 数据收录条数

		#如果过有运维权限，根据可管理的项目查询
		elif user_from_db.has_perm('release.change_ops_release'):
			projectid_list = list(user_with_project.objects.filter(user_id=auth_return[1]).values_list('project_id'))  # 项目ID
			# 字符拼接成Q或查询,
			orselect = or_select('project_id', projectid_list)  # 说明（这里是release表中的上线id）： 字段名，列表
			# 执行或查询
			if orselect == 0:
				release_data = []
				select_total = 0
			else:
				release_data = release.objects.filter(orselect).order_by('-id')[id_start:id_end]
				select_total = release.objects.filter(orselect).order_by('-id').count()
				# 处理数据库读出来的数据
				display_data = deal_display_data(release_data)

			release_list = Paging(current_page,
								  columns_table,
								  pageing_nub,
								  select_total)  # 传参说明：当前页，表显示列数，分页显示数, 数据收录条数


	# 返回分页数据表列表，分页显示页列表，分页总数, 数据查询数据条数
	return render(request, 'listrequest.html', {'left_nav': auth_return[0],
												'current_page': current_page,
												'display_data': display_data,
												'release_list': release_list})
