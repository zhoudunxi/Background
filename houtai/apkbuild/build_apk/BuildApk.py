#coding=UTF-8

import sys
import os
import re
import shutil
import commands
import paramiko
from  PurgeCdn import PurgeCdn
from ConfigParser import ConfigParser as Config
#from sendMail import SendMail
from time import time
from threading import Timer


class BuildApk(object):
	"""	
	Build a new apk file by updating the configure file of the origin apk file.
	Require:
		GLIBC: 2.14
		apktool: 2.2.4
	"""

	def __init__(self, runuser, version, lists):
		#The work directory.
		#self.chroot = sys.path[0] + os.sep
		self.chroot = os.getcwd() + os.sep
		#Read the configure files.
		#config_dir = self.chroot + 'apkbuild' + os.sep +'configs'
		config_dir = self.chroot + 'configs'
		config_file = config_dir + os.sep + 'BuildApk.conf'
		conf = Config()
		conf_temp = conf.read(config_file)
		if not conf_temp:
			print('\033[31mPlease check the configure file: %s\033[0m'%config_file)
			sys.exit(2)

		#The 'keystore' key for signning.
		self.sign_key = config_dir + os.sep + 'sign_key' + os.sep + 'sdjj.keystore'
		try:
			os.stat(self.sign_key)
		except OSError as e:
			print('\033[31m%s\033[0m'%e)
			sys.exit(2)
			
		#The directory of running time.
		self.runtime = self.chroot + 'runtime'
		#The user of running as.
		self.runuser = runuser
		#The directory of running time for user.
		self.runuserdir = self.runtime + os.sep + self.runuser + os.sep
		#The version of APK.
		self.version = version
		#The identify names of APK. 
		self.lists = lists
		#The path of downloading the apk file.
		self.remote_origin = conf.get('backends', 'remote_origin_apk_path')
		#The storage hosts for apk files.
		self.hosts = conf.get('backends', 'hosts').split(',')
		##The ssh port, username and private key file of the backends.
		self.port = int(conf.get('backends', 'port'))
		self.user = conf.get('backends', 'user')
		self.key = conf.get('backends', 'key')
		#The strings of private key for SSH connection by the paramiko module.
		try:
			self.pkey = paramiko.RSAKey.from_private_key_file(self.key)
		except Exception as err:
			print('\033[31m%s\033[0m'%err)
			#sys.exit(2)
		#The command tool of decompiling and compiling the apk.
		self.apktool = conf.get('default', 'apktool')
		#The command tool of signning the apk.
		self.jarsigner = conf.get('default', 'jarsigner')
		#The command tool of decompression.
		self.unzip = conf.get('default', 'unzip')
		#The command tool of compression.
		self.zip = conf.get('default', 'zip')
		#The password for signning.
		self.sign_password = conf.get('default', 'sign_password')
		#The alias name of the apk file.
		self.alias = conf.get('default', 'alias')
		#The directory for storaging the origin apk file.
		self.origin_temp = self.runuserdir + 'origin'
		#The directory for decompilation.
		self.decompile_temp = self.runuserdir + 'decompile'
		#The directory for compilation.
		self.compile_temp = self.runuserdir + 'compile'
		#The directory for signning.
		self.sign_temp = self.runuserdir + 'sign'
		#The directory for decompression.
		self.unzip_temp = self.runuserdir + 'unzip'
		#The directory for compression.
		self.zip_temp = self.runuserdir + 'zip'
		#The local origin apk file.
		self.origin = self.origin_temp + os.sep
		#The apk files directory in the remote hosts.
		self.remote_root_dir = conf.get('backends', 'remote_root_dir')
		#The url of accessing the apk file.
		self.pre_url = conf.get('default', 'pre_url')
		#The mail server address.
		self.mail_server = conf.get('default', 'mail_server')
		#The user of the mail from.
		self.mail_from = conf.get('default', 'mail_from')
		#Create the directory of running time for user.
		self.online_users = conf.get('default', 'online_users')

	def initialize(self):
		"""Initialize the variables and environments."""

		print('\033[32mInitializing......\033[0m')
		#try:
			#The max online users.
		#	if len(os.listdir(self.runtime)) > int(self.online_users):
		#		return 2
		#except:
		#	os.mkdir(self.runtime)
		#Initialize environments for user.
		def __inituser():
			os.mkdir(self.runuserdir)
			#Time mark.
			with open(self.runuserdir + "mark.tmp", 'w') as mark:
				mark.write(str(time()).split('.')[0])
			for dir in (self.origin_temp, 
				self.decompile_temp, 
				self.compile_temp, 
				self.sign_temp, 
				self.unzip_temp, 
				self.zip_temp):
				os.mkdir(dir)

		try:
			os.listdir(self.runuserdir)
			try:
				with open(self.runuserdir + "mark.tmp", 'r') as oldmark:
					oldMark = int(oldmark.read())
				#If one task time is more than one hour, then initialize repeatable.
				if int(str(time()).split('.')[0]) - oldMark > 3600:
					shutil.rmtree(self.runuserdir)
					__inituser()
				else:
					raise NameError() 
					#return 1
			except:
				print '%s 用户已经存在，正在删除用目录' %self.runuserdir
				shutil.rmtree(self.runuserdir)
				__inituser()
		except:
			__inituser()


	def get_origin_apk(self):
		"""
		Get the origin apk file from the storage host.
		"""
		remote_origin_apk = self.remote_origin + 'sdjj-%s.apk' %self.version 
		conn = paramiko.SSHClient()  
		conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
		conn.connect(self.hosts[0], port=self.port, 
			username=self.user, pkey=self.pkey, timeout=30)  
		sftp = conn.open_sftp()
		try:
			sftp.get(remote_origin_apk, 
				self.origin_temp + os.sep + 'sdjj-%s.apk' %self.version)
		except:
			print("\033[31mThe file %s in %s: No such file.\033[0m"%(
				remote_origin_apk, self.hosts[0]))
			sys.exit(3)

	def decompile(self, list):
		"""
		Decompile the apk file.
		"""
		origin_apk = self.origin + 'sdjj-%s.apk' %self.version

		commands.getoutput('%s d -o %s/%s %s'%(self.apktool, 
			self.decompile_temp, list, origin_apk))

	def update_configure(self, list):
		"""
		Update the configure file of the apk.
		"""
		with open('%s/%s/AndroidManifest.xml'%(self.decompile_temp, list), 'r') as xml:
			data = xml.read()
		new_data = re.sub(r'UMENG_CHANNEL\" android:value=\".*\"',
			'UMENG_CHANNEL\" android:value=\"%s\"'%list, data)	
		with open('%s/%s/AndroidManifest.xml'%(self.decompile_temp, list), 'w') as new_xml:
			new_xml.write(new_data)
	
	def compile(self, list):
		"""
		Compile the apk file.
		"""
		commands.getoutput('%s b -o %s/%s.apk %s/%s'%(self.apktool, self.compile_temp, 
			list, self.decompile_temp, list))
	
	def sign(self, list):
		"""
		Sign the apk file again.
		"""
		sign_cmd = "/bin/echo '%s' | %s -verbose -keystore %s -signedjar %s/%s.apk %s/%s.apk %s"%(
			self.sign_password, self.jarsigner, self.sign_key, self.sign_temp, 
			list, self.compile_temp, list, self.alias)
		commands.getoutput(sign_cmd)

	def unzip_origin_apk(self):
		"""
		Unzip the origin apk file.
		"""
		origin_apk = self.origin + 'sdjj-%s.apk' %self.version

		commands.getoutput('%s %s -d %s'%(self.unzip, origin_apk, self.origin_temp))
		
	def unzip_signned_apk(self, list):
		"""
		Unzip the signned apk file.
		"""
		commands.getoutput('%s %s/%s.apk -d %s/%s'%(self.unzip, 
			self.sign_temp, list, self.unzip_temp, list))

	def restore_service_dir(self, list):
		"""
		Restore the 'service' directory to the configed apk files from the origin apk files.
		"""
		shutil.copytree('%s/META-INF/services'%self.origin_temp, 
			'%s/%s/META-INF/services'%(self.unzip_temp, list))	

	def zip_signned_apk(self, list):
		"""
		Zip the signned apk files.
		"""
		os.chdir(self.unzip_temp + os.sep + list)
		commands.getoutput('%s -r %s/%s.apk *'%(self.zip, self.zip_temp, list))
		os.chdir(self.chroot)
		

	def distribute(self, list):
		"""
		Distribute the builded apk files.
		"""
		failist = []
		for host in self.hosts:
			try:
				conn = paramiko.SSHClient()
				conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				conn.connect(host, port=self.port, username=self.user, 
					pkey=self.pkey, timeout=30)
				sftp = conn.open_sftp()
			except:
				return {'result':1, 'message':'网络连接失败，请联系管理员！'}

			try:
				sftp.stat(self.remote_root_dir + list)
				try:
					sftp.put(self.zip_temp + os.sep + list + '.apk',
						self.remote_root_dir + list + os.sep + 'sdjj.apk')
					#If it's a updated apk file, then purge CDN.
					#if host == self.hosts[0]:
					#	cdn = PurgeCdn()
					#	status = cdn.baishan('url', self.pre_url + list + '/sdjj.apk')
					#	if status == 1:
					#		failist.append(list)
				except:
					failist.append(list)
			except:
				try:
					sftp.mkdir(self.remote_root_dir + list)
					sftp.put(self.zip_temp + os.sep + list + '.apk',
						self.remote_root_dir + list + os.sep + 'sdjj.apk')
				except:
					failist.append(list)
			sftp.close()
			conn.close()

		return {'result':0, 'message':failist}

	def clear(self):
		"""
		Clear the temporary data.
		"""
		print('\033[32mClear the temporary data......\033[0m')
		shutil.rmtree(self.runuserdir)	
		print('\033[33mDone successful.\033[0m')

	def run(self):
		result = self.initialize()
		if result:
			return result
		print('\033[32mDoing, please wait......\033[0m')
		def __run():
			self.get_origin_apk()
			self.unzip_origin_apk()

			#for list in self.lists:
				#list = list.strip('\r\n')
			list = self.lists
			self.decompile(list)
			self.update_configure(list)
			self.compile(list)
			self.sign(list)
			self.unzip_signned_apk(list)
			self.restore_service_dir(list)
			self.zip_signned_apk(list)
			failist = self.distribute(list)

			self.clear()

			#Mail the result.
			if failist['result'] == 1:
				send_msg = failist['message']
			elif failist['result'] == 0:
			#	send_msg = '您提交的渠道包已更新，更新成功的如下：\n%s\n\n更新失败的如下，您可以尝试重新提交：\n%s\n'%('\n'.join(set(self.lists) - set(failist['message'])), '\n'.join(set(failist['message'])))
				send_msg = '\n成功：%s \n失败：%s\n' %(self.lists, failist['message'])
			print send_msg 
		__run()
		#	send = SendMail(self.mail_server, self.mail_from)
		#	send.mail(self.runuser + '@shandjj.com', '渠道包更新', send_msg)
		#Async by the timer.
		#timer = Timer(1,__run)
		#timer.start()
		#return 0

