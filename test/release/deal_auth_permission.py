# -*- coding: utf-8 -*-

#导入django的模型User表，因为认证用的是django的
from django.contrib.auth.models import User
from project_manegement.models import project
from project_manegement.models import storage
from release.models import release
from public.log import log

def permission_control(doing,userid):
    try:
        user_db = User.objects.get(id=userid)
    except Exception as err:
        log('warning', 'select sql failure: %s' % err.message)
    perm = False
    if not doing:
        if user_db.is_staff or user_db.has_perm('release.change_release') or user_db.has_perm('release.change_activity_release'):
            perm = True
    elif doing == 'carry_sql':  # dba执行完sql
        if user_db.is_staff or user_db.has_perm('release.change_dba_release') or user_db.has_perm('release.change_activity_release'):
            perm = True
    elif doing == 'prepare':  # 满足发预发布条件
        if user_db.is_staff or user_db.has_perm('release.change_ops_release') or user_db.has_perm('release.change_activity_release'):
            perm = True
    elif doing == 'dev_tested':  # 开发测试通过
        if user_db.is_staff or user_db.has_perm('release.change_release') or user_db.has_perm('release.change_activity_release'):
            perm = True
    elif doing == 'online':  # 满足发正式条件
        if user_db.is_staff or user_db.has_perm('release.change_ops_release') or user_db.has_perm('release.change_activity_release'):
            perm = True
    elif doing == 'toback':  # 满足回滚条件
        if user_db.is_staff or user_db.has_perm('release.change_ops_release') or user_db.has_perm('release.change_activity_release'):
            perm = True
    return perm


def get_pre_env(requestid):
    try:
        project_id = release.objects.get(id=requestid).project_id
        storage_id = project.objects.get(id=project_id).storage_id
        pre_env = storage.objects.get(id=storage_id).branch_name
	return_date = True
	if pre_env == 'test':
		return_data = False
	elif pre_env == 'master':
		return_data = True
	return return_data
    except Exception as err:
        log('warning', 'select sql failure: %s' % err)
	
