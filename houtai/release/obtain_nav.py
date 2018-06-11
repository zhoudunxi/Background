# -*- coding: utf-8 -*-
#导入数据库模块,从数据库读取导航列表
from release.models import left_nav
#导入用户表，这里用于赋权
from django.contrib.auth.models import User
def _listdate(left_title, left_list):
	left_class = 'homeactive2'
        #if left_list.left_nav_title.encode("utf-8") == '管理app服务器':
	if left_list.left_nav_title.encode("utf-8") == left_title:
		left_class = 'active'
	#将标题和url和css传递给模板
	return (left_list.left_nav_pid, left_list.left_nav_title, left_list.left_nav_url, left_class)

def header_left_nav(left_title,userid=1):
        #通过排序查找所有列
        left_nav_db = left_nav.objects.order_by('left_nav_sort')
        #用循环的方式将列中的数据，写入到列表中，为了给模板通过list.0这种方式调用
	user_display = ('代码提交','请求列表','帮助')
	dba_ops_user = ('请求列表','帮助')
	apk_display = ('更新APK','APK队列','帮助')
	user = User.objects.get(id=userid)
        left_return = []
        for left_list in left_nav_db:
		Title = left_list.left_nav_title.encode('utf-8')	
		if user.is_staff: #管理员用户
			left_return.append(_listdate(left_title,left_list))
		else:
			if user.has_perm('release.change_release') and Title in user_display or user.has_perm('release.change_activity_release') and Title in user_display: #有release项目的change_release权限用户
				left_return.append(_listdate(left_title,left_list))
			if user.has_perm('apkbuild.change_apk_build_queue') and Title in apk_display:#有apkbuild 的can_apkbuild的用户
				left_return.append(_listdate(left_title,left_list))
			if user.has_perm('release.change_dba_release') or user.has_perm('release.change_ops_release'):
				if Title in dba_ops_user:
					left_return.append(_listdate(left_title, left_list))
        #return render_to_response('management_server.html',{'header_nav':header_return, 'left_nav':left_return})
	#将从数据库里获取到的数据用元组的返回给程序
        return left_return
