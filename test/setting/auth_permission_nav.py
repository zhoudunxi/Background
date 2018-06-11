# -*- coding: utf-8 -*-

#导入‘数据库读取导航列表’模块
from release.obtain_nav import header_left_nav
# 导入django session模型，用于取出userid
from django.contrib.sessions.models import Session
#导入django的模型User表，因为认证用的是django的
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect



@csrf_protect
def AUTH_Perm(request, leftnav):  # 认证权限
    session_key = request.session.session_key  # 获取sessionid
    userid = Session.objects.get(pk=session_key).get_decoded()['_auth_user_id']  # 更加sessionid查找出userid，根据userid做权限控制
    left_nav_db = header_left_nav(leftnav, userid)  # 调用模块，获取返回左导航元组数据

    # 获取用户id，用户权限控制
    user_db = User.objects.get(id=userid)
    is_staff = user_db.is_staff  # 用户身份
    # change_release = user_db.has_perm('apkbuild.can_apkbuild') #用户权限
    return (left_nav_db, userid, is_staff)