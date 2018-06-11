# -*- coding: utf-8 -*-
from django import forms

#这样做只是为了排序
def user_return(user_perm):
	identity = [('User', '开发'), ('DBAuser','DBA用户'), ('Opsuser','运维'), (True, '管理员'), ('APKuser', 'apk更新用户'), ('Activityuser', '活动开发')]
	if user_perm == 'Admin':
		user_perm = (True, '管理员')
	if user_perm == 'User':
		user_perm = ('User', '开发')
	if user_perm == 'APKuser':
		user_perm = ('APKuser', 'apk更新用户')
	if user_perm == 'DBAuser':
		user_perm = identity[1]
	if user_perm == 'Opsuser':
		user_perm = identity[2]
	if user_perm == 'Activityuser':
		user_perm = identity[5]
	del identity[identity.index(user_perm)]
	identity.insert(0,user_perm)
	return  identity

class User_Form(forms.Form):
	#identity choices 支持列表和元祖，False代表普通用户，True代表普通用户,后面是其他用户通过赋权控制
	#identity = [(False,'用户'),(True,'管理员'),('APKuser','apk更新用户')]
	identity = user_return('User')
	username = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder':'*必填-建议字母','class':'form-control input-md'}),label='登陆名')
	last_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder':'*必填','class':'form-control input-md'}),label='中文名')
	email = forms.EmailField(max_length=60,widget=forms.TextInput(attrs={'placeholder':'*必填','class': 'form-control input-md'}),label='邮箱')
	is_staff = forms.ChoiceField(choices=identity,required=False,widget=forms.Select(attrs={'class':'form-control input-md','style':'width:150px'}),label='用户身份')
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control input-md'}),label='密码')
	trypassword = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control input-md'}),label='确认密码')

