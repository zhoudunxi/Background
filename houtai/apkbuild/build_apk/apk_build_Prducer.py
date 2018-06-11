#!/bin/env python
#coding: utf-8
#单一测试rabbitmq
import pika, sys

username = 'xiaocheng'
version = '2.3.0'


body_m = int(sys.argv[1]) #body 数
Dic = int(sys.argv[2]) #队列优先级

# 建立一个实例
credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(
	pika.ConnectionParameters('8.8.8.90',5672,'/',credentials)
	)
# 声明一个管道，在管道里发消息
channel = connection.channel()

priority = {'x-max-priority':100} #优先级 ，

# 在管道里声明queue
channel.queue_declare(queue='apk_build_queue', durable=True, arguments=priority) #arguments添加参数这里添加优先级,队列优先级
# RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
I = 56
while I <= body_m:
	#body 用户名：版本号：渠道号：优先级
	channel.basic_publish(exchange='',
				routing_key='apk_build_queue',
				body="%s:%s:mqbuild%s:%s" %(username, version, I, Dic), 
				properties=pika.BasicProperties(delivery_mode=2,priority=Dic) #这里是消息优先级，这里是重点
			)  # 消息内容
	I += 1
	#print(" [x] Sent 'H'")
connection.close()  # 队列关闭
