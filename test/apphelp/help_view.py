# -*- coding: utf-8 -*-
#django http模块
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
#导入‘认证权限和导航’模块
from setting.auth_permission_nav import AUTH_Perm

#导入‘数据库读取导航列表’模块
#from release.obtain_nav import header_left_nav
# 导入django session模型，用于取出userid 
#from django.contrib.sessions.models import Session

@csrf_protect
@login_required(login_url='/login/')
def Help(request):
        #if not request.user.is_authenticated(): #校验是否认证，如果没有认证跳转到登陆页面
                #return HttpResponseRedirect('/login/?next=%s' % request.path)
        # session_key = request.session.session_key #获取sessionid
        # userid = Session.objects.get(pk=session_key).get_decoded()['_auth_user_id'] #更加sessionid查找出userid，根据userid做权限控制
        # left_return = header_left_nav('帮助',userid) #调用模块，获取返回左导航元组数据

        auth_return = AUTH_Perm(request,'帮助')

        return render(request,'help.html',{'left_nav':auth_return[0]})
