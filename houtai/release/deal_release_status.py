# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Permission
#数据库表
from setting.models import ops_duty, user_with_project
from release.models import dev_release, release, dba_release, ops_release
#共用配置文件
from public.configs import getconfig
from public.log import log


#上线的状态，从数据库获取
def css_release_status(release_data,requestid):
    release_status = release_data['release_status'].encode('utf-8')
    submitter = release_data['developer_name'].encode('utf-8')
    # dba或者运维处理
    return_data = {'untreated':['btn-info',submitter],
                   'carry_sql':['btn-secondary-outline','DBA'],
                   'prepare':['btn-secondary-outline','运维'],
                   'dev_tested':['btn-secondary-outline','开发'],
                   'online':['btn-secondary-outline','运维'],
                   'done': ['btn-secondary-outline','完成'],
                   'toback':['btn-secondary-outline','回滚']}
    #dba 处理
    try:
        dba_db_data = dba_release.objects.get(request_id=requestid)
        if dba_db_data.sql_action_status:
            return_data['carry_sql'][0] = 'btn-info'
            return_data['carry_sql'][1]= User.objects.get(id=dba_db_data.dba_user_id).last_name
    except Exception as err:
        log('warning', 'select sql failure: %s' % err.message)

    #运维处理
    try:
        ops_db_data = ops_release.objects.get(request_id=requestid)
	release_db_data = release.objects.get(id=requestid)
        if ops_db_data.ops_to_pre_status:
	    if release_db_data.release_status == u'预发布失败':
                return_data['prepare'][0] = 'btn-warning'
	    else:
                return_data['prepare'][0] = 'btn-info'
            return_data['prepare'][1] = User.objects.get(id=ops_db_data.pre_user_id).last_name
        if ops_db_data.ops_to_online_status:
	    if release_db_data.release_status == u'发布失败':
            	return_data['online'][0] = 'btn-warning'
	    else:
            	return_data['online'][0] = 'btn-info'
            return_data['done'][0] = 'btn-success'
            return_data['online'][1] = User.objects.get(id=ops_db_data.online_user_id).last_name
        if ops_db_data.ops_toback_status:
	    if release_db_data.release_status == u'回滚失败':
            	return_data['toback'][0] = 'btn-warning'
	    else:
            	return_data['toback'][0] = 'btn-danger'
            return_data['toback'][1] = User.objects.get(id=ops_db_data.toback_user_id).last_name
    except Exception as err:
        log('warning', 'select sql failure: %s' % err.message)

    #开发处理
    try:
        dev_db_data = dev_release.objects.get(request_id=requestid)
        if dev_db_data.dev_to_online_status:
            return_data['dev_tested'][0] = 'btn-info'
            return_data['dev_tested'][1] = User.objects.get(id=dev_db_data.dev_user_id).last_name
    except Exception as err:
            log('warning', 'select sql failure: %s' % err.message)

    return return_data


