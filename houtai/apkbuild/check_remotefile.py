#!/bin/env python
#coding: utf-8
#检查远程文件服务器上，文件是否存在
import os, sys, paramiko
from ConfigParser import ConfigParser as Config



config_file = os.getcwd() + os.sep + 'apkbuild' + os.sep + 'configs' + os.sep + 'BuildApk.conf' 
conf = Config()
conf_temp = conf.read(config_file)
if not conf_temp:
	print('\033[31mConfigure file: %s  is not find\033[0m'%config_file)
	sys.exit(2)

#远程文件服务器配置
ssh_filehost = conf.get('backends', 'hosts').split(',')
ssh_fileport = int(conf.get('backends', 'port'))
ssh_fileuser = conf.get('backends', 'user')
ssh_filekey = conf.get('backends', 'key')
remote_root_dir = conf.get('backends', 'remote_root_dir') #远程apk包所在的绝对路径


#校验apk文件是否在远程服务器存在
def Check_File(remote_file):
	remote_file =  remote_root_dir + remote_file
	pkey = paramiko.RSAKey.from_private_key_file(ssh_filekey)
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname=ssh_filehost[0], port=ssh_fileport, username=ssh_fileuser, pkey=pkey)
	#到文件服务器执行shell命令，文件存在返回1，不存在返回0
	stdin, stdout, stderr = ssh.exec_command("CHECK_F=%s;if [[ -f $CHECK_F ]];then echo '1';else echo '0';fi" %remote_file)
	#print(stdout.read())
	#print(stderr.read())
	#处理返回数据，因为返回的数据里有多余的行\n,我只要第一行的数据
	sshout = []
	for Line in stdout.readline():
		sshout.append(Line)
	#print int(sshout[0])
	ssh.close()
	return sshout[0]

#remote_file =  remote_root_dir + 'sdjj-2.4.0.apk' 
#a=Check_File(remote_file)
#print a
