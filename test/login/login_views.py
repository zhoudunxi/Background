# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from login.forms import Login_Contact
#导入django 认证模块
from django.contrib import auth
from django.contrib.auth.models import User #djando user表

def Login(request):
	form_login = Login_Contact()
	nextpath = request.GET.get('next')#get到的路径传给前端，前端再post到后端来。
	if nextpath == None:
		nextpath = '/release/'
	if request.method == 'POST':
		form_login = Login_Contact(request.POST)
		if form_login.is_valid():
			login_data = form_login.cleaned_data #清理成Unicode对象,一个字典
			nextpath = request.POST.get('nextpath') #获取跳转的url路径
			userauth = auth.authenticate(username=login_data['username'],password=login_data['password']) #验证用户信息
			if userauth is not None and userauth.is_active:
				auth.login(request, userauth) #登陆session写入django框架
				request.session.set_expiry(0) #设置session超时时间，这里是0,表示浏览器关闭session结束
				user = User.objects.get(username=login_data['username'])
				if not user.is_staff and user.has_perm('apkbuild.change_apk_build_queue') and nextpath == u'/release/':#重新定义apk用户的url
					nextpath = '/apkupdate/'
				if not user.is_staff and user.has_perm('release.change_dba_release') and nextpath == u'/release/':
					nextpath = '/requestlist/'
				if not user.is_staff and user.has_perm('release.change_ops_release') and nextpath == u'/release/':
					nextpath = '/requestlist/'
				return HttpResponseRedirect(nextpath)
			else: #返回报错到login页面
				autherror = "少年，您的用户名或者密码错误！"
				return render(request,'login.html',{'form_login':form_login,'autherror':autherror})
				
	return render(request,'login.html',{'form_login':form_login,'nextpath':nextpath})

def Logout(request):#登出
	auth.logout(request)
	return HttpResponseRedirect('/login/')
