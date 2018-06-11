#coding:UTF-8

import sys, os, json
import urllib, urllib2


class PurgeCdn(object):
	"""调用CDN API推送缓存。"""

	def __init__(self):
		#帝联用户标识码
		self.dl_token = '436bd7e7'
		self.dl_baseurl = 'http://push.dnion.com/cdnUrlPush.do'
		#白山用户标识码
		self.bs_token = 'ead97defe505571d7e1fc5ce339dfad1'
		self.bs_baseurl = 'https://api.qingcdn.com/v1/domain/purge/purges?&token='
		#七牛用户标识码
		self.SK = "z6EKysuplbymn3FpCZig3eY12BoVbD0vq4zvTBud"
		self.AK = "jbbgUn5jnyxwivgpzBvc_v1tw6_lgTN1O9WmGcxj"
		self.qn_baseurl = "http://fusion.qiniuapi.com/v2/tune/refresh"
		get_qn_token = "/usr/bin/echo '/v2/tune/refresh' | "+\
        		"/usr/bin/openssl dgst -binary -hmac %s -sha1 | "%(self.SK)+\
        		"/usr/bin/base64 | "+\
       			"/usr/bin/tr + - | "+\
        		"/usr/bin/tr / _"
		self.qn_token = os.popen(get_qn_token).read().strip("\n")


	@staticmethod
	def __url_split(f,url):
		"""一次只能处理100个URL地址，如果多于100个URL地址则按100为单位切片年理。"""

		url_list = url.split(',')
		if len(url_list) <= 100:
			f(url)
		else:
			i = 0
			for i in range(len(url_list)):
				if i + 100 > len(url_list):
					f(','.join(url_list[i:len(url_list)]))
					break
				else:
					f(','.join(url_list[i:i+100]))
					i = i + 100
		
	def dilian(self,type,url):
		"""帝联CDN推送。
		：param type:string，dir为目录，url为URL。
		：param url:string，URL地址，多个用英文逗号分隔。"""
				
		if type == 'url':
			type = 1
		elif type == 'dir':
			type = 0
		params = urllib.urlencode({'captcha':self.dl_token,'type':type,'url':url})
		try:
			urllib2.urlopen(self.dl_baseurl,params,timeout=120)
			return 0
		except:
			return 1

	def baishan(self,type,url):
		"""白山CDN推送。
		：param type:string，dir为目录，url为URL。
		：param url:string，URL地址，多个用英文逗号分隔。"""

		params = urllib.urlencode({'type':type,'urls[]':url})
		try:
			urllib2.urlopen(self.bs_baseurl+self.bs_token,params,timeout=120)
			return 0
		except: 
			return 1

	def qiniu(self,type,url):
		"""七牛CDN推送
		params:
			type: string, url为URL，dir为目录。
			url:  string, URL地址，多个用英文逗号分隔。如果是目录，每个地址后面需以'/'结尾。
		"""
       		
		req = urllib2.Request(self.qn_baseurl) 
		req.get_method = lambda: 'POST'
		if type == "url":
			data = json.dumps({"urls":["%s"%url]})
		elif type == "dir":
			data = json.dumps({"dirs":["%s"%url]})
		req.add_header("Content-Type", "application/json")
		req.add_header("Authorization", "QBox %s:%s"%(self.AK, self.qn_token))
		req.add_data(data)
		try:
			resp = urllib2.urlopen(req, timeout=30)
			return 0
		except:
			return 1


#if __name__=="__main__":
	#obj = PurgeCdn()
	#obj.dilian('url','http://static.shandjj.com/website/default/images/phone1.png')
	#obj.baishan('url','http://download.shandjj.com/apk/t1.txt')
	#obj.qiniu('url', 'http://download.shandjj.com/apk/sdjj.apk')
		
