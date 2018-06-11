#!/bin/env python
#coding: utf-8
#RabbiMQ生产，将消息写入到rabbitmq
import pika, os, sys
from ConfigParser import ConfigParser as Config

config_file = os.getcwd() + os.sep + 'apkbuild' + os.sep + 'configs' + os.sep + 'BuildApk.conf' 
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

def APK_Production(message_id, apk_version, identify, message_priority, project_name):
	# 建立一个实例
	connection = pika.BlockingConnection(
		pika.ConnectionParameters(RabbitMQIP,int(RabbitMQPort),'/',credentials)
		)
	# 声明一个管道，在管道里发消息
	channel = connection.channel()
	# 在管道里声明queue，持久化，队列优先级
	channel.queue_declare(queue=APKqueue, durable=True, arguments=queue_priority) #arguments添加参数这里添加优先级,队列优先级
	channel.basic_publish(exchange='',
				routing_key=APKqueue,
				body="%s:%s:%s:%s:%s" %(message_id, apk_version, identify, message_priority, project_name), #body-->消息ID：版本号：渠道标识：优先级
				properties=pika.BasicProperties(delivery_mode=2,priority=message_priority) #这里是消息优先级，这里是重点
			)  # 消息内容
	connection.close()  # 队列关闭
