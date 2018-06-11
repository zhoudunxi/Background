#!/bin/env python
#coding: utf-8
#获取队列状态
import urllib, urllib2,json
url = "http://8.8.8.90:15672/api/queues"

password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
password_mgr.add_password(None, url, 'admin', 'admin')
handler = urllib2.HTTPBasicAuthHandler(password_mgr)
opener = urllib2.build_opener(handler)
opener.open(url)
urllib2.install_opener(opener) 
response = urllib2.urlopen(url)
print (response.read())
