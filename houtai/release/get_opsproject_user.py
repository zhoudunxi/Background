# -*- coding: utf-8 -*-
#根据上线ID，查找当前能上线的运维，先找项目运维，当项目运维请假了，就找大佬

from django.contrib.auth.models import User, Permission
#数据库表
from setting.models import ops_duty, user_with_project
from release.models import dev_release, release, dba_release, ops_release
#共用配置文件
from public.configs import getconfig


def ops_for_project_user(requestid):
    project_id = release.objects.get(id=requestid).project_id
    project_user = user_with_project.objects.filter(project_id=project_id).values_list('user_id')
    retuen_date = []
    n_leave = len(project_user)
    for user_id in project_user:
        try:
            User_db = User.objects.get(id=int(user_id[0]))  # 取出用户数据
        except:
            n_leave -= 1
            continue
        if User_db.has_perm('release.change_ops_release'):  # 如果有运维权限
            on_duty = ops_duty.objects.get(user_id=User_db.id).duty_status
            if not on_duty:  # 以前是值班，现在用于请假，如果运维没有请假
		name_email = (User_db.last_name,User_db.email)
                retuen_date.append(name_email)
            else:#运维请假了
                n_leave -= 1
        else:
            n_leave -= 1
            continue


    if n_leave == 0: #所有项目运维请假了，就获取运维大佬名字
        cn_name = getconfig('sendemail', 'ops_default_cn')
	email = getconfig('sendemail', 'ops_default_email')
        retuen_date.append((cn_name.decode('utf-8'),email.decode('utf-8')))
    return retuen_date
