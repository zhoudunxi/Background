# -*- coding: utf-8 -*-
#django http模块
from setting.models import user_with_project
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
def __all_permissions():
    all_permissions = ['release.change_release',
                       'apkbuild.change_apk_build_queue',
                       'release.change_dba_release',
                       'release.change_ops_release']
    return all_permissions

#普通用户提升权限到管理员，拥有所有权，添加除自己以外的权限
def user_up_to_admin(current_perm,edituserid):
    all_permissions = __all_permissions()
    user_data = User.objects.get(id=edituserid)
    user_data.is_staff = True
    del all_permissions[all_permissions.index(current_perm)] #重点。
    for perm in all_permissions:
        perm = perm.split('.')[1]
        change_perm = Permission.objects.get(codename=perm) #权限是多对多的表，必须先取出权限在添加。
        user_data.user_permissions.add(change_perm)
    user_data.save()

#普通用户（包括管理员）切换到普通用户，去除掉多余权限
def user_up_to_user(current_perm,edituserid):
    all_permissions = __all_permissions()
    user_data = User.objects.get(id=edituserid)
    del all_permissions[all_permissions.index(current_perm)]
    for perm in all_permissions:
        if user_data.has_perm(perm):
            perm = perm.split('.')[1]
            change_perm = Permission.objects.get(codename=perm)
            user_data.user_permissions.remove(change_perm)
    if not user_data.has_perm(current_perm): #赋权
        current_perm = current_perm.split('.')[1]
        change_perm = Permission.objects.get(codename=current_perm)
        user_data.user_permissions.add(change_perm)
    if user_data.is_staff:
        user_data.is_staff = False
    user_data.save()

#普通用户修改成开发，需要移除项目
def user_delete_project(edituserid):
    from_db_projectid = user_with_project.objects.filter(user_id=edituserid).values_list('project_id')
    for db_pro in from_db_projectid:
        get_u_p = user_with_project.objects.filter(user_id=edituserid, project_id=db_pro[0])
        get_u_p.delete()