# -*- coding: utf-8 -*-
#django http模块
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound #404
#解决编码问题，返回中文,对上下文内容进行重用
from django.template import RequestContext
#导入‘数据库读取导航列表’模块
#from release.obtain_nav import header_left_nav
from setting.auth_permission_nav import AUTH_Perm
#导入表单
from project_manegement.forms import Storage_Form, Project_Form, Storage_Edit_Form
#导入数据库模型
from project_manegement.models import storage, project
from django.contrib.auth.models import User #用户认证表
#django 将model转换为字典
from django.forms.models import model_to_dict
#读取cmdb项目信息
from public.get_cmdb_info import deal_group
# 导入django session模型，用于取出userid 
from django.contrib.sessions.models import Session


@csrf_protect
@login_required(login_url='login')
def Project_mana(request):
        # if not request.user.is_authenticated(): #校验是否认证，如果没有认证跳转到登陆页面
        #         return HttpResponseRedirect('/login/?next=%s' % request.path)
        # session_key = request.session.session_key #获取sessionid
        # userid = Session.objects.get(pk=session_key).get_decoded()['_auth_user_id'] #更加sessionid查找出userid，根据userid做权限控制
        # left_return = header_left_nav('项目管理',userid) #调用模块，获取返回左导航元组数据

        #获取用户id，用户权限控制
        #is_staff = User.objects.get(id=userid).is_staff #用户身份

    auth_return = AUTH_Perm(request,'项目管理')
    if not auth_return[2]:#非管理员用户跳转到发布页面
             return HttpResponseNotFound('<h1>ERROR:404 少年！没事不要乱输入url！</h1>')
    if request.method == 'GET': #如果有get数据，就执行数据操作，这里是删除
		get_storageid = request.GET.get('deletestorage')
		get_projectid = request.GET.get('deleteproject')
		if get_storageid:
			storage.objects.filter(id=get_storageid).delete()
		if get_projectid:
			project.objects.filter(id=get_projectid).delete()
    storage_data = storage.objects.all()
    project_data_db = project.objects.all()
    project_data = []
    for data_list in project_data_db: #因为projec表中记录的是storageid我们需要找到仓库名返回给前端
		data_list = model_to_dict(data_list)
		data_list['storage_id'] = storage.objects.get(id=data_list['storage_id']).name
		project_data.append(data_list)
    return_date = {
        'left_nav': auth_return[0],
        'storage_data': storage_data,
        'project_data': project_data
    }
    return render(request,'projectmanegement.html',return_date)

@csrf_protect
@login_required(login_url='login')
def ADD_storage(request):
    auth_return = AUTH_Perm(request, '项目管理')
    if not auth_return[2]:#非管理员用户跳转到发布页面
         return HttpResponseNotFound('<h1>ERROR:404 少年！没事不要乱输入url！</h1>')
    storage_form = Storage_Form() #获取表单
    # 如果是用POST提交来的表单
    if request.method == 'POST':
            #将表单里的数据写入变量
        storage_form = Storage_Form(request.POST)
        if storage_form.is_valid():
            storage_data = storage_form.cleaned_data#清理成Unicode对象,一个字典
            storage_to_db = storage(**storage_data)
            storage_to_db.save()
            #return HttpResponseRedirect('/123/')
            add_status = 'success'
            return render(request,'project_addstorage.html',
                {'left_nav':auth_return[0],
                 'storage_form':Storage_Form() ,
                 'add_status':add_status})
    return render(request,'project_addstorage.html',
                  {'left_nav':auth_return[0],
                   #'cmdb_group':deal_group(),
                'storage_form':storage_form})

@csrf_protect
@login_required(login_url='login')
def EDIT_storage(request):
    auth_return = AUTH_Perm(request, '项目管理')
    if not auth_return[2]:#非管理员用户跳转到发布页面
         return HttpResponseNotFound('<h1>ERROR:404 少年！没事不要乱输入url！</h1>')
    # 左侧导航栏
    return_data = {'left_nav': auth_return[0]}
    if request.method == 'GET':
        storage_id = request.GET.get('id')
        try:
            storage_obj = storage.objects.get(id=storage_id)
            return render(request, 'project_editstorage.html',
                          {'left_nav': return_data['left_nav'],
                           'storage_id':storage_id,
                           'name':storage_obj.name,
                           'back_path': storage_obj.back_path,
                           'description': storage_obj.description,
                           'git_path': storage_obj.git_path,
                           'staging_path': storage_obj.staging_path,
                           'sync_script': storage_obj.sync_script,
                           'branch_name': storage_obj.branch_name,
                           'enable_pre_env': storage_obj.enable_pre_env,
                           'staging_path_for_pre': storage_obj.staging_path_for_pre,
                           'sync_script_for_pre': storage_obj.sync_script_for_pre})
        except:
            return redirect('/projectmanegement/')
    else:
        try:
            id = request.POST.get('storage_id')
        except:
            return redirect('/projectmanegement/')
        #将表单里的数据写入变量
        storage_form = Storage_Edit_Form(request.POST)
        if storage_form.is_valid():
            post_data = storage_form.cleaned_data#清理成Unicode对象,一个字典
            # 更新数据至数据库
            storage.objects.filter(id=id).update(
                back_path = post_data['back_path'],
                description = post_data['description'],
                git_path = post_data['git_path'],
                staging_path = post_data['staging_path'],
                sync_script = post_data['sync_script'],
                branch_name = post_data['branch_name'],
                enable_pre_env = post_data['enable_pre_env'],
                staging_path_for_pre = post_data['staging_path_for_pre'],
                sync_script_for_pre = post_data['sync_script_for_pre'])
            #返回处理状态
            return_data['edit_status'] = 'success'
            return render(request,'project_editstorage.html',return_data)
        else:
            return_data['edit_status'] = 'invalid'
            return render(request, 'project_editstorage.html', return_data)

@csrf_protect
@login_required(login_url='login')
def ADD_project(request):
    auth_return = AUTH_Perm(request, '项目管理')
    if not auth_return[2]:  # 非管理员用户跳转到发布页面
        return HttpResponseNotFound('<h1>ERROR:404 少年！没事不要乱输入url！</h1>')
    cmdb_group = deal_group()
    return_date = {
        'left_nav': auth_return[0],
        'cmdb_group': cmdb_group,
        'project_form': Project_Form()}
    # 如果是用POST提交来的表单
    if request.method == 'POST':
        #将表单里的数据写入变量
        project_form = Project_Form(request.POST)
        if project_form.is_valid():
            cmdb_group_form = request.POST.get('project_name').split(':')
            project_data = project_form.cleaned_data#清理成Unicode对象,一个字典
            project_data['project_name'] = cmdb_group_form[1]
            project_data['cmdb_group_id'] = cmdb_group_form[0]
            project_data['storage_id'] = int(project_data['storage_id'])
            project_to_db = project(**project_data)
            project_to_db.save()
            return_date['add_status'] = 'success'
            return render(request,'project_addproject.html',return_date)
    return render(request,'project_addproject.html',return_date)

@csrf_protect
@login_required(login_url='login')
def EDIT_project(request):
    auth_return = AUTH_Perm(request, '项目管理')
    if not auth_return[2]:  # 非管理员用户跳转到发布页面
        return HttpResponseNotFound('<h1>ERROR:404 少年！没事不要乱输入url！</h1>')
    #左侧导航栏
    return_data = {'left_nav': auth_return[0]}
    if request.method == 'GET':
        project_id = request.GET.get('id')
        try:
            project_obj = project.objects.get(id=project_id)
            git_repo_name = storage.objects.get(id=project_obj.storage_id).name
            return render(request, 'project_editproject.html',
                          {'left_nav': return_data['left_nav'],
                           'project_id':project_id,
                           'project_name': project_obj.project_name,
                           'project_description': project_obj.project_description,
                           'project_label': project_obj.project_label,
                           'project_remote_path': project_obj.remote_path,
                           'project_pre_remote_path': project_obj.pre_remote_path,
                           'storage_id': project_obj.storage_id,
                           'git_repo_name': git_repo_name})
        except:
            return redirect('/projectmanegement/')
    else:
        try:
            id = request.POST.get('project_id')
        except:
            return redirect('/projectmanegement/')
        #将表单里的数据写入变量
        project_form = Project_Form(request.POST)
        if project_form.is_valid():
            post_data = project_form.cleaned_data#清理成Unicode对象,一个字典
            # 更新数据至数据库
            project.objects.filter(id=id).update(
                project_name = request.POST.get('project_name'),
                project_description = post_data['project_description'],
                project_label = post_data['project_label'],
		remote_path = post_data['remote_path'],
		pre_remote_path = post_data['pre_remote_path'])
            #返回处理状态
            return_data['edit_status'] = 'success'
            return render(request,'project_editproject.html',return_data)
        else:
            return_data['edit_status'] = 'invalid'
            return render(request, 'project_editproject.html', return_data)
