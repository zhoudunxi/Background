#!/bin/env python
#coding: utf-8
#单一测试rabbitmq

import time, os, sys
import multiprocessing, pika
from ConfigParser import ConfigParser as Config
import paramiko
import BuildApk


config_file = os.getcwd() + os.sep + 'configs' + os.sep + 'BuildApk.conf' 
conf = Config()
conf_temp = conf.read(config_file)
if not conf_temp:
	print('\033[31mConfigure file: %s  is not find\033[0m'%config_file)
	sys.exit(2)

#消息队列服务器配置
RabbitMQIP = conf.get('RabbitMQ','mqhost')
RabbitMQPort = conf.get('RabbitMQ','mqport')
RabbitMQUser = conf.get('RabbitMQ','mquser')
RabbitMQPWD = conf.get('RabbitMQ','mqpwd')
credentials = pika.PlainCredentials(RabbitMQUser, RabbitMQPWD)
APKqueue = conf.get('RabbitMQ','apkqueue') #apk制作的队列名
CDNqueue = conf.get('RabbitMQ','cdnqueue') #刷新CDN的队列名
Process = int(conf.get('RabbitMQ','process')) #开启多进程，这里是进程数，一个进程对应一个work
queue_priority = {'x-max-priority':100} #队列优先级

#远程文件服务器配置
ssh_filehost = conf.get('backends', 'hosts').split(',')
ssh_fileport = int(conf.get('backends', 'port'))
ssh_fileuser = conf.get('backends', 'user')
ssh_filekey = conf.get('backends', 'key')
remote_root_dir = conf.get('backends', 'remote_root_dir') #远程apk包所在的绝对路径

#校验apk文件是否在远程服务器存在
def Check_APK_File(remote_file):
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
		#print '123%s' %Line
		sshout.append(Line)
	#print int(sshout[0])
	ssh.close()
	return sshout[0]

#更新cdn-queue，body，--> 用户名：版本号：渠道标识：优先级：是否新文件
def Publish_cdn(body, priority): #body  消息，priority优先级
	connection1 = pika.BlockingConnection(pika.ConnectionParameters(RabbitMQIP,int(RabbitMQPort),'/',credentials))
	channel1 = connection1.channel() # 声明一个管道，在管道里发消息
	##完成apk跟新后将队列重新加入cdn更新队列中
	channel1.queue_declare(queue=CDNqueue, durable=True, arguments=queue_priority) #durable表示持久化,arguments订阅了队列优先级
	channel1.basic_publish(
		exchange='',
		routing_key=CDNqueue,
		properties=pika.BasicProperties(delivery_mode=2,priority=priority), 
		body=str(body)) #delivery_mode消息持久化，priority表示消息的优先级
	connection1.close()

#APK打包, 消费的回调函数真正打包的调用在这个函数里
def callback(ch, method, properties, body):  # 四个参数为标准格式
	#print(ch, method, properties)  
	ITme = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	print("%s Received %r" %(ITme, body))
	split_body = body.split(":")
	#先调用校验函数，如果远程文件不存在
	remote_file = remote_root_dir + split_body[2] + os.sep + 'sdjj.apk'
	file_status = Check_APK_File(remote_file)
	split_body.append(file_status) #文件状态加入到消息列表，0文件不存在，1文件存在
	username = split_body[0] + split_body[2]
	Main = BuildApk.BuildApk(username, split_body[1], split_body[2]) #初始化
	Main.run()#执行apk打包
	#file_status = Check_APK_File(remote_file)  #打包后检查文件是否生成
	body = ':'.join(split_body) #将列表转换长字符用户:分隔，--> 用户名：版本号：渠道标识：优先级：是否新文件
	Publish_cdn(body,int(split_body[3])) #加入到cdn队列
	ch.basic_ack(delivery_tag = method.delivery_tag)  # 告诉生成者，消息处理完成
	print "ACK 完美: %r" %body
		
	#ch.close()
	#connection.close()

#APK打包，消费
def APK_Consume():
#	time.sleep(1)
	connection = pika.BlockingConnection(pika.ConnectionParameters(RabbitMQIP,int(RabbitMQPort),'/',credentials))
	channel = connection.channel() # 声明一个管道，在管道里发消息
	channel.basic_qos(prefetch_count=1) #一次订阅一个数据，MQ只会get一个数据
	channel.queue_declare(queue=APKqueue, durable=True, arguments=queue_priority)# 在管道里声明queue,队列优先级
	channel.basic_consume(callback,queue=APKqueue,) #定义消费回调函数，和消费队列
	channel.start_consuming() # 开始消费消息，阻塞式消费



print(' [*] APK-Consume Program starts executing......')
#out = Check_APK_File('/data/shandjjdownload/apk/mqbuild14/sdjj.apk')
#print out
APK_Consume()

#pool = multiprocessing.Pool(Process)
#while True:
#	pool.apply_async(APK_Consume)
#pool.close()
#pool.join()

