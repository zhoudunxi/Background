#!/bin/env python
#coding: utf-8
#消费cdn

import time
import multiprocessing, pika


RabbitMQIP = '8.8.8.90'
RabbitMQPort = '5672'
credentials = pika.PlainCredentials('admin', 'admin')
#APKqueue = 'apk_build_queue'
CDNqueue = 'cdn_renew_queue' #队列名称
Process = 20 #进程数,这里一次执行20条


def callback(ch, method, props, body):
	ITme = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	print("%s Received %r" %(ITme, body))
	time.sleep(1)
	
	
	ch.basic_ack(delivery_tag = method.delivery_tag)
	ch.close()
	print 'ACK --%r' %body
	
def CDNconsumer():
	connection = pika.BlockingConnection(pika.ConnectionParameters(RabbitMQIP,int(RabbitMQPort),'/',credentials))
	channel = connection.channel()
	channel.basic_qos(prefetch_count=1)
	channel.basic_consume(
		callback,
		queue=CDNqueue,
	)
	connection.process_data_events()
	connection.close()
print "[-start-] 开始执行"
#CDNconsumer()

Pool = multiprocessing.Pool(Process)
Count = 1
while Count <= Process:
	Pool.apply_async(CDNconsumer)
	Count += 1
Pool.close()
Pool.join()
