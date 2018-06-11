# -*- coding: utf-8 -*-
#调用django的认证机制，创建权限
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

def UpdateAPKPers():
	#这三个字段分别表示 模型的用户化名称，模型所属app名称，模型名称,对应数据库django_content_type，这里我建一个空模型，用于控制apk更新的权限
	content_type =  ContentType.objects.create(name='apkpermission', app_label='apkbuild', model='apkpermision') 
	#三个字段分别表示,自定义的权限名称，所对应的content-tpye，代码调用的权限名称（这个很重要）
	can_apkbuild = Permission.objects.create(name='can apkbuild', content_type=content_type, codename='can_apkbuild')
	return can_apkbuild
