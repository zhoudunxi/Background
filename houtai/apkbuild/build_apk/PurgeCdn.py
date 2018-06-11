#coding:UTF-8

import sys
import urllib,urllib2


class PurgeCdn(object):
	"""调用CDN API推送缓存。"""

	def __init__(self):
		#帝联用户标识码
		self.dl_token = '436bd7e7'
		self.dl_baseurl = 'http://push.dnion.com/cdnUrlPush.do'
		#白山用户标识码
		self.bs_token = 'ead97defe505571d7e1fc5ce339dfad1'
		self.bs_baseurl = 'https://api.qingcdn.com/v1/domain/purge/purges?&token='

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
        


#if __name__=="__main__":
	#obj = PurgeCdn()
	#obj.dilian('url','http://static.shandjj.com/website/default/images/phone1.png')
	#obj.baishan('url','http://download.shandjj.com/apk/t1.txt')
		
