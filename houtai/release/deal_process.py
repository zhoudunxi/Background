# -*- coding: utf-8 -*-
# 流程处理，未处理--预发布--正式
from release.models import release, dba_release, ops_release, dev_release
from cmdb.models import cmdbmanage
from project_manegement.models import project, storage
import os, time, datetime, tarfile, shutil, json
from get_opsproject_user import ops_for_project_user
#from git import Repo
from public.UploadFiles import UploadFiles
#获取cmdb 中的hosts
from cmdb.cmdbviews import Cmdb_group
#打日志模块
from public.log import log

#未处理阶段，用户提交了请求后，将数据替换处理后返回给前端
def untreated(RequestID):
	try:
		release_data = release.objects.get(id=RequestID) #根据请求的ID，从数据库中获取发布数据
	except Exception as err:
		log('warning', 'select sql failure: %s' %err.message)
	description_data = release_data.description #描述
	release_data.description = description_data.split('\r\n') #描述格式化成列表
	filelist_data = release_data.filelist#文件列表
	release_data.filelist =  filelist_data.replace('\\','/').split()#文件列表将\替换成/，再格式化成列表
	begin_CSTtime = release_data.begin_time + datetime.timedelta(hours=+8) #转换成东八区时间
	release_data.begin_time = begin_CSTtime.strftime('%Y-%m-%d %H:%M:%S') #时间转换
	if release_data.last_time: #如果有数据就转换时间
		last_CSTtime = release_data.last_time + datetime.timedelta(hours=+8)
		release_data.last_time = last_CSTtime.strftime('%Y-%m-%d %H:%M:%S')
	try:
		project_data = project.objects.get(id=release_data.project_id)
		storage_id = project_data.storage_id
		storage_data = storage.objects.get(id=storage_id)
	except Exception as err:
		log('warning', 'select sql failure: %s' %err.message)
		project_data = ''
		storage_data = ''
	dba_release_data = ''
	if release_data.is_have_sql:
		dba_release_data = dba_release.objects.get(request_id=RequestID) #取出sql
	 	dba_release_data.sql_statement = dba_release_data.sql_statement.split('\r\n') #格式化sql
	ops_user_list = ops_for_project_user(RequestID) #获取项目运维
	return (release_data, storage_data, dba_release_data, ops_user_list, project_data)

#git pull ,文件打包备份，复制文件到镜像目录
def BACKUPCOPY(RequestID,ENV):
	return_data = 'success'
	untreated_data = untreated(RequestID) #获取未处理数据
	file_list = untreated_data[0].filelist #文件列表
	storage_data = untreated_data[1] #获取仓库表数据
	#os.chdir('%s' %storage_data.git_path) #切换到git仓库目录
	#os.system('git pull origin %s' %untreated_data[1].branch_name)#pull所有代码,分支来自数据库
	try:
		repo = Repo(storage_data.git_path)
		#如果当前分支不是仓库表中分支，切换分支
		if repo.head.reference.name != untreated_data[1].branch_name:
			repo.git.checkout(untreated_data[1].branch_name)
		repo.remote().pull()
	except Exception as err:
		log('warning', 'Remote git repository exception: %s' %err.message)
		return_data = 'faild'
		return return_data
	backup_path_m = storage_data.back_path + time.strftime('/%Y/%m', time.localtime()) #拼接备份目录到月份
	if os.path.isdir(backup_path_m) == False:	#如果没有日期备份目录，创建目录
		os.makedirs(backup_path_m)
	#os.chdir(backup_path) #切换到备份目录
	git_file = [] #git仓库的文件
	backup_path = [] #备份目录
	pre_stag_file= [] #预发布镜像目录
	stag_file = [] #需要复制到的镜像目录
	for lists in file_list: #拼接要备份的文件，绝对路径
		file_relative = os.path.sep + lists
		git_files = storage_data.git_path + file_relative
		backup_paths = '%s%s%s%s%s' %(backup_path_m, os.path.sep, RequestID, os.path.sep, os.path.dirname(lists))
		if untreated_data[1].enable_pre_env.encode('utf-8') == 'true': #如果开启了预发布
			pre_stag_files = storage_data.staging_path_for_pre + file_relative
			pre_stag_file.append(pre_stag_files)
		stag_files = storage_data.staging_path + file_relative
		git_file.append(git_files)
		#print backup_paths
		backup_path.append(backup_paths)
		stag_file.append(stag_files)
	if ENV == 'init':
		log('info', 'release_id: %s file backup and Copy the files to the pre-release mirrored directory' %RequestID)
		LICOUNT = 0
		#print git_file
		for file_path in git_file:#将所有要备份的文件，复制到Request目录,复制到镜像目录
			#第一步将镜像文件备份到备份目录
			#print stag_file[LICOUNT]
			log('info','release_id: %s 1 copy %s --> %s' %(RequestID,stag_file[LICOUNT], backup_path[LICOUNT]))
			if os.path.isfile(stag_file[LICOUNT]) == True:
				if os.path.isdir('%s' %backup_path[LICOUNT]) == False:
					os.makedirs(backup_path[LICOUNT])
				#os.system('/bin/cp -a %s %s' %(stag_file[LICOUNT], backup_path[LICOUNT]))
				shutil.copy2(stag_file[LICOUNT], backup_path[LICOUNT])
				#print 'copy %s --> %s' %(stag_file[LICOUNT], backup_path[LICOUNT])

			#第二步，将新文件从git仓库复制到镜像目录
			if pre_stag_file: #如果开启了预发布
				pre_stag_file_path = os.path.dirname(pre_stag_file[LICOUNT])
				if os.path.isdir(pre_stag_file_path) == False:
					os.makedirs(pre_stag_file_path)
				#os.system('/bin/cp -a %s %s' %(file_path, pre_stag_file_path))
				try:
					shutil.copy2(file_path, pre_stag_file_path)
				except:
					pass
				#print 'copy %s --> %s' %(file_path, pre_stag_file_path)
				log('info', 'release_id: %s 2 copy %s --> %s' %(RequestID,file_path, pre_stag_file_path))
			LICOUNT = LICOUNT + 1
		#tar 打包压缩备份目录
		bak_path = '%s%s%s' %(backup_path_m,os.path.sep,RequestID)
		# os.system('tar -zcf %s.tar.gz %s --remove-files' %(RequestID, RequestID)) #打包压缩文件
		tar = tarfile.open((bak_path + '.tar.gz'), 'w:gz') #指定包名
		for root, dir, files in os.walk(bak_path):#指定了备份目录
			for file in files:
				fullpath = os.path.join(root, file)
				tar.add(fullpath)
		tar.close()
		#os.system('rm -rf %s' %RequestID)#删除临时文件夹
		if os.path.isdir(bak_path):
			shutil.rmtree(bak_path)
	if ENV == 'online': #需要更新正式的时候才将仓库文件更新到正式的镜像目录
		log('info', 'release_id: %s Copy the files to the online-release mirrored directory' % RequestID)
		LICOUNT1 = 0
		for file_path1 in git_file:
			stag_file_path = os.path.dirname(stag_file[LICOUNT1])
			if os.path.isdir(stag_file_path) == False:
				os.makedirs(stag_file_path)
			#os.system('/bin/cp -a %s %s' %(file_path1, stag_file_path))
			try:
				shutil.copy2(file_path1, stag_file_path)
			except:
				pass
			LICOUNT1 = LICOUNT1 + 1
	return return_data

def __UPFILE(untreated_data,source_path,env):
	try:
		project_db = project.objects.get(id=untreated_data[0].project_id)
	except Exception as err:
		log('warning', 'select sql failure: %s' %err.message)
	if env == 'pre': #预发布
		env = 1002
		remote_path = project_db.pre_remote_path
	elif env == 'online':#正式
		env = 1000
		remote_path = project_db.remote_path
	hosts = json.loads(Cmdb_group(untreated_data[4].cmdb_group_id,env))['server_ip']
	files = {}
	for db_file in untreated_data[0].filelist:
		source_file = source_path + os.path.sep + db_file
		#如果项目目录与上传文件目录一样，去掉文件目录，一般是多项目在一个仓库的问题
	 	##label_list = untreated_data[4].project_label.split('/')
	 	#db_file_list = db_file.split('/')
	 	#db_file = ('/').join(set(db_file_list) - set(label_list))
	 	#远程目录+/+未处理的文件或者目录
	 	##remote_file = project_db.remote_path + os.path.sep + db_file
		if untreated_data[4].project_label:
			#这里使用字符串裁剪的办法，#截取第n个字符到结尾
			label_len = len(untreated_data[4].project_label)
			remote_file = remote_path + db_file[label_len:]
		else:
			remote_file = remote_path + os.path.sep + db_file
	 	files[source_file] = remote_file
	log('info','source_file--remote_file %s' %files)
	if hosts:
		upfiles = UploadFiles(hosts,files) #调用磊哥的上线模块
		uploads_status = upfiles.uploadfiles()
		updata_ops_release = ops_release.objects.get(request_id=untreated_data[0].id)
		updata_ops_release.upload_file_status = str(uploads_status)
		updata_ops_release.save()
		if uploads_status['uploaderror'] or uploads_status['establisherror'] or uploads_status['syntaxerror'] or uploads_status['nonexistent']:
			uploads_status = 'faild'
		else:
	 		uploads_status = 'success'
	else:
		uploads_status = 'faild'
	return uploads_status
	

def UPDATECODE(RequestID): #发布代码，调用rsync脚本同步代码
	untreated_data = untreated(RequestID)
	#project_label = project.objects.get(id=untreated_data[0].project_id).project_label #获取标签，脚本调用的位置变量，
	if untreated_data[1].enable_pre_env.encode('utf-8') == 'true': #如果开启了预发布
		if untreated_data[0].release_status.encode('utf-8') == '未处理' or untreated_data[0].release_status.encode('utf-8') == '已执行SQL':
			source_path = untreated_data[1].staging_path_for_pre
			uploads_status = __UPFILE(untreated_data,source_path,'pre') #上传文件
			return uploads_status
			#sync_script = untreated_data[1].sync_script_for_pre
			#os.system('%s %s' %(sync_script, project_label))	
		if untreated_data[0].release_status.encode('utf-8') == '开发已测试':
			BACKUPCOPY(RequestID,ENV='online') #建代码复制到正式的镜像目录 
			source_path = untreated_data[1].staging_path
			uploads_status = __UPFILE(untreated_data,source_path,'online') #上传文件
			return uploads_status
			#sync_script = untreated_data[1].sync_script
			#os.system('%s %s' %(sync_script, project_label))	
			

	else: #没开启预发布，一般是测试环境。
		untreated_data = untreated(RequestID)
		BACKUPCOPY(RequestID,ENV='online') #建代码复制到正式的镜像目录 
		source_path = untreated_data[1].staging_path
		uploads_status = __UPFILE(untreated_data,source_path,'online') #上传文件
		return uploads_status
		#sync_script = untreated_data[1].sync_script #获取a返回数据中的sync_script脚本路径，
		#os.system('%s %s' %(sync_script, project_label))	

#解压备份的文件，复制到镜像目录
def ROLBACK(RequestID):
	untreated_data = untreated(RequestID)
	begin_date = untreated_data[0].begin_time.split('-')
	backup_path = untreated_data[1].back_path + os.path.sep + begin_date[0] + os.path.sep + begin_date[1] #备份目录到RequestID的创建日期
	tarfile.open((backup_path + os.path.sep + str(RequestID) + '.tar.gz')).extractall(path=(backup_path + os.path.sep + str(RequestID)))
	backup_file = []
	pre_stag_path = []
	stag_path = []
	for listf in untreated_data[0].filelist:
		back_filef = backup_path + os.path.sep + str(RequestID) + backup_path + os.path.sep + str(RequestID) + os.path.sep +listf #备份文件，绝对路径
		if untreated_data[1].enable_pre_env.encode('utf-8') == 'true': #如果开启了预发布
			pre_target_path = '%s/%s' %(untreated_data[1].staging_path_for_pre, os.path.dirname(listf)) #预发布镜像目录
			pre_stag_path.append(pre_target_path)
		target_path = '%s/%s' %(untreated_data[1].staging_path, os.path.dirname(listf)) #镜像目录
		backup_file.append(back_filef)
		stag_path.append(target_path)
	PHCOUNT = 0	
	for bak_file in backup_file:
		if os.path.isfile(bak_file) == True:
			if pre_stag_path: #如果预发布文件存在
				shutil.copy2(bak_file, pre_stag_path[PHCOUNT])
			shutil.copy2(bak_file, stag_path[PHCOUNT])
		PHCOUNT = PHCOUNT + 1
	shutil.rmtree(backup_path + os.path.sep + str(RequestID))

def BACKCODE(RequestID): #回滚代码
	untreated_data = untreated(RequestID)
	project_label = project.objects.get(id=untreated_data[0].project_id).project_label #获取标签，脚本调用的位置变量，
	#pre_sync_script = untreated_data[1].sync_script_for_pre #预发布脚本名称
	if untreated_data[1].enable_pre_env.encode('utf-8') == 'true': #如果开启了预发布
		if untreated_data[0].release_status.encode('utf-8') == '已发布':
			ROLBACK(RequestID) #执行解压，复制
			#sync_script = untreated_data[1].sync_script #正式脚本名称
			#os.system('%s %s' %(sync_script, project_label)) #同步到正式	
			#os.system('%s %s' %(pre_sync_script, project_label))	#同步到预发布
			uploads_status = __UPFILE(untreated_data, untreated_data[1].staging_path, 'online') #同步到正式 
			uploads_status_pre = __UPFILE(untreated_data, untreated_data[1].staging_path_for_pre, 'pre') #同步到预发布
			return uploads_status
		if untreated_data[0].release_status.encode('utf-8') == '已预发布':
			ROLBACK(RequestID) #执行解压，复制
			#os.system('%s %s' %(pre_sync_script, project_label)) #同步到预发布
			uploads_status_pre = __UPFILE(untreated_data, untreated_data[1].staging_path_for_pre, 'pre') #同步到预发布
			return uploads_status_pre	
	else: 
		ROLBACK(RequestID) #执行解压，复制
		#untreated_data = untreated(RequestID)
		#sync_script = untreated_data[1].sync_script #获取a返回数据中的sync_script脚本路径，
		#os.system('%s %s' %(sync_script, project_label))	
		uploads_status = __UPFILE(untreated_data, untreated_data[1].staging_path, 'online') #同步到正式 
		#uploads_status_pre = __UPFILE(untreated_data, untreated_data[1].staging_path_for_pre, 'pre') #同步到预发布
		return uploads_status



#上线主表
def releasetable(RequestID,status,userid):
	#       release.objects.filter(id=RequestID).update(last_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) #表更新，单字段更新
	try:
		release_update = release.objects.get(id=RequestID) #表更新，多字段更新
	except Exception as err:
		log('warning', 'select sql failure: %s' %err.message)
	release_update.last_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	release_update.release_status = status
	#release_update.last_name = userid
	release_update.last_user_id = userid
	release_update.save()

#dba 上线表
def dba_releasetable(requestid,userid):
	try:
		update = dba_release.objects.get(request_id=requestid)
	except Exception as err:
		log('warning', 'select sql failure: %s' %err.message)
	update.dba_user_id = userid
	update.sql_action_status = 1
	update.save()

#运维上线表
def ops_releasetable(requestid,userid,pare):

	if pare == 'prepare':
		try:
			update = ops_release.objects.get(request_id=requestid)
		except Exception as err:
			log('warning', 'select sql failure: %s' % err.message)
		update.pre_user_id = userid
		update.ops_to_pre_status = 1
		update.save()
	elif pare == 'online':
		try:
			update = ops_release.objects.get(request_id=requestid)
		except Exception as err:
			log('warning', 'select sql failure: %s' % err.message)
		update.online_user_id = userid
		update.ops_to_online_status = 1
		update.save()

#开发确认状态表
def dev_releasetable(requestid,userid):
	try:
		update = dev_release.objects.get(request_id=requestid)
	except Exception as err:
		log('warning', 'select sql failure: %s' %err.message)
	update.dev_user_id = userid
	update.dev_to_online_status = 1
	update.save()

def ops_toback(requestid,userid):
	try:
		update = ops_release.objects.get(request_id=requestid)
	except Exception as err:
		log('warning', 'select sql failure: %s' %err.message)
	update.toback_user_id = userid
	update.ops_toback_status = 1
	update.save()
