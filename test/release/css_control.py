# -*- coding: utf-8 -*-
#流程控制中的，权限控制模块
from release.deal_auth_permission import permission_control



#控制上线的按钮
def css_control(release_data,enable_pre_env,is_have_sql,user_id):
	release_status = release_data['release_status'].encode('utf-8')
	css_data = {'sbimit_name_time':False,
				'have_sql':False,
				'btn_sql':False,
				'btn_pre':False,
				'btn_dev_t':False,
				'btn_ol':False,
				'btn_back':False}

	if is_have_sql:  # 如果有sql
		if permission_control('',user_id):
			css_data['have_sql'] = True

	#dba或者运维处理,以下是对按钮的处理
	if release_status == '未处理':
		#调用权限模块，控制上线的按钮显示
		if permission_control('carry_sql',user_id) or permission_control('prepare',user_id):
			if is_have_sql: #如果有sql
				if permission_control('carry_sql',user_id):
					css_data['btn_sql'] = True
			else:
				if enable_pre_env != 'true': #如果不开启预发布，就直接显示上线按钮
					css_data['btn_ol'] = True
				else:
					css_data['btn_pre'] = True
	#开发处理
	elif release_status == '已预发布':
		if permission_control('dev_tested',user_id):
			css_data['sbimit_name_time'] = True
			css_data['btn_dev_t'] = True
		if permission_control('prepare',user_id):
			css_data['sbimit_name_time'] = True
                        #css_data['btn_dev_t'] = True
			css_data['btn_back'] = True

	#运维处理
	elif release_status == '开发已测试':
		if permission_control('online',user_id):
			css_data['sbimit_name_time'] = True
			css_data['btn_ol'] = True
			css_data['btn_back'] = True
	elif release_status == '已执行SQL':
		if permission_control('prepare',user_id):
			css_data['btn_pre'] = True
	elif release_status == '已发布':
		if permission_control('toback',user_id):
			css_data['sbimit_name_time'] = True
			css_data['btn_back'] = True
	elif release_status == '已回滚':
		css_data['sbimit_name_time'] = True
	return css_data


