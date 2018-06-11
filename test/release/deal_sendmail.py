# -*- coding: utf-8 -*-
#处理上线过程中的邮件发送 上线提交--sql上线--运维上线到预生产--开发确认--运维上线到正式
#发邮件模块
from public.sendMail import SendMail
from django.contrib.auth.models import User, Permission
#数据库表
from setting.models import ops_duty, user_with_project
from release.models import dev_release, release, dba_release, ops_release
#共用配置文件
from public.configs import getconfig
#获取项目运维
from release.get_opsproject_user import ops_for_project_user


#发送邮件给dba
def send_to_dba(requestid):
    release_data = __release_select(requestid) #上线表
    last_name = release_data.developer_name #开发名字
    description = release_data.description #上线描述
    dba_per = Permission.objects.get(codename='change_dba_release')
    emails = User.objects.filter(user_permissions=dba_per).values('email', 'last_name','username')
    for mail in emails:
	if mail['username'] == u'admin':
		continue
        email_add = mail['email']
        mail_cn_name = mail['last_name'].encode('utf-8')
        msg = '程序猿%s提交上线请求，请尽快审核sql并操作。<br><br>&emsp;&emsp;&emsp;更新说明:%s' % (last_name.encode('utf-8'), description.encode('utf-8'))
        sendmail = SendMail('127.0.0.1', 'operations')
        # 参数说明 收件人，主题，收件人称呼，邮件正文
        sendmail.mail(email_add, 'SQL审核并上线', mail_cn_name, msg)


#发送邮件给运维
# def send_to_ops(requestid,putsql,nextpare):
#     on_duty = ops_duty.objects.filter(duty_status=1).values('user_id')
#     release_data = __release_select(requestid)
#     last_name = release_data.developer_name
#     description = release_data.description
#     for user_id in on_duty:
#         email = User.objects.get(id=user_id['user_id'])
#         mail_cn_name = email.last_name.encode('utf-8')
#
#         if nextpare == 'prepare':
#             if putsql == 'have':
#                 user_id = dba_release.objects.get(request_id=requestid).dba_user_id
#                 last_name = User.objects.get(id=user_id).last_name
#                 msg = 'DBA已经将SQL执行，请尽快审核并将代码提交到预发布。<br><br>&emsp;&emsp;&emsp;更新说明:%s' % (
#                     last_name.encode('utf-8'), description)
#             else:
#                 msg = '程序猿%s提交上线请求，请尽快审核并将代码提交到预发布。<br><br>&emsp;&emsp;&emsp;更新说明:%s' % (
#                     last_name.encode('utf-8'), description)
#             mail_object = '上线请求，请提交至预发布环境'
#         elif nextpare == 'online':
#             msg = '程序猿%s已经测试完成，请尽快审核并将代码提交到正式。<br><br>&emsp;&emsp;&emsp;更新说明:%s' % (last_name.encode('utf-8'), description)
#             mail_object = '上线请求，请提交至正式环境'
#         sendmail = SendMail('127.0.0.1', 'operations')
#         # 参数说明 收件人，主题，收件人称呼，邮件正文
#         sendmail.mail(email.email, mail_object, mail_cn_name, msg)
def send_to_ops(requestid,putsql,nextpare):
    #on_duty = ops_duty.objects.filter(duty_status=1).values('user_id')
    release_data = __release_select(requestid) #上线表
    last_name = release_data.developer_name #开发名字
    description = release_data.description #上线描述
    ops_user = ops_for_project_user(requestid) #获取项目运维，里面包括用（户中文名，email）
    for user_list in ops_user:
	email_addr = user_list[1] #邮件接收人
	mail_cn_name = user_list[0] #接收人中文名
	#参数说明：请求id，下个流程，是否有sql，收件人地址，收件人中文名，上线描述
	__ops_sendemail(requestid,nextpare,putsql,email_addr,mail_cn_name.encode('utf-8'),last_name,description)


#发送邮件给开发
def send_to_dev(requestid,pare,uploads_status):
    dev_user_id = dev_release.objects.get(request_id=requestid).dev_user_id
    email = User.objects.get(id=dev_user_id)
    mail_cn_name = email.last_name.encode('utf-8')
    release_data = __release_select(requestid)
    description = release_data.description
    if pare == 'prepare':
        user_id = ops_release.objects.get(request_id=requestid).pre_user_id
        last_name = User.objects.get(id=user_id).last_name
	if uploads_status == 'success':
        	msg = '项目运维%s已经将代码上线到预发布，请尽快测试。<br><br>&emsp;&emsp;&emsp;更新说明:%s' % (last_name.encode('utf-8'), description.encode('utf-8'))
		mail_object = '您有代码被上到预发布'
	else:
        	msg = '警告！项目运维%s上线代码到预发布，失败！请尽快联系项目运维。<br><br>&emsp;&emsp;&emsp;更新说明:%s' % (last_name.encode('utf-8'), description.encode('utf-8'))
		mail_object = '您有代码到预发失败'
		
    elif pare == 'online':
	user_id = ops_release.objects.get(request_id=requestid).online_user_id
	last_name = User.objects.get(id=user_id).last_name
	if uploads_status == 'success':	
        	msg = '恭喜！更新已经完成！项目运维：%s<br><br>&emsp;&emsp;&emsp;更新说明:%s' % (last_name.encode('utf-8'), description.encode('utf-8'))
		mail_object = '您的代码已经上线完成'
	else:
        	msg = '警告！更新正式失败！尽快登陆运维工具查看状态。项目运维：%s <br><br>&emsp;&emsp;&emsp;更新说明:%s' %(last_name.encode('utf-8'), description.encode('utf-8'))
		mail_object = '您的代码上线正式失败'
    elif pare == 'toback':
        user_id = ops_release.objects.get(request_id=requestid).toback_user_id
        last_name = User.objects.get(id=user_id).last_name
	if uploads_status == 'success':
        	msg = '警告！您的代码已经被%s回滚！<br><br>&emsp;&emsp;&emsp;更新说明:%s' % (last_name.encode('utf-8'), description.encode('utf-8'))
		mail_object = '您的代码已经被回滚'
	else:
        	msg = '警告！您的代码已经被%s回滚！但是失败了！！<br><br>&emsp;&emsp;&emsp;更新说明:%s' % (last_name.encode('utf-8'), description.encode('utf-8'))
		mail_object = '您的代码回滚失败'
		

    sendmail = SendMail('127.0.0.1', 'operations')
    # 参数说明 收件人，主题，收件人称呼，邮件正文
    sendmail.mail(email.email, mail_object, mail_cn_name, msg)

#获取上线描述
def __release_select(requestid):
    data = release.objects.get(id=requestid)
    data.description = data.description.split()  # 描述格式化成列表
    data.description = ('<br>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;').join(data.description)	
    return data

#发邮件
def __ops_sendemail(requestid,nextpare,putsql,email_addr,mail_cn_name,last_name,description):
	if nextpare == 'prepare':
	    if putsql == 'have':
		user_id = dba_release.objects.get(request_id=requestid).dba_user_id
		last_name = User.objects.get(id=user_id).last_name
		msg = 'DBA已经将SQL执行，请尽快审核并将代码提交到预发布。<br><br>&emsp;&emsp;&emsp;更新说明:%s' %description.encode('utf-8')
	    else:
		msg = '程序猿%s提交上线请求，请尽快审核并将代码提交到预发布。<br><br>&emsp;&emsp;&emsp;更新说明:%s' % (
			last_name.encode('utf-8'), description.encode('utf-8'))
	    mail_object = '上线请求，请提交至预发布环境'
	elif nextpare == 'online':
	    msg = '程序猿%s已经测试完成，请尽快审核并将代码提交到正式。<br><br>&emsp;&emsp;&emsp;更新说明:%s' % (last_name.encode('utf-8'), description.encode('utf-8'))
	    mail_object = '上线请求，请提交至正式环境'
	sendmail = SendMail('127.0.0.1', 'operations')
	# 参数说明 收件人，主题，收件人称呼，邮件正文
	sendmail.mail(email_addr, mail_object, mail_cn_name, msg)
