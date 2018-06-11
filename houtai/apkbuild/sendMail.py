#coding=UTF-8

import smtplib,sys
from email.mime.text import MIMEText
from email.header import Header

class SendMail(object):
	"""发送邮件"""

	def __init__(self, mail_server, mail_from):
		#邮件服务器
		self.mailserver = mail_server
		#发件人
		self.mailfrom = mail_from

	def mail(self, mail_to, subject, username):
		"""发送邮件"""
		#整合邮件正文，包括发件人，收件人，主题等邮件元数据。
		#msg = MIMEText(msg,'plain','utf-8')
		msg = ('<html><body>',
			'<p>您好：%s</p>' %username,
			#'<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;有上线，请及时处理！</p>',
			'<p>&emsp;&emsp;&emsp;有上线，请及时处理！</p>',
			'<h3>温馨提示：这是一封系统邮件，请勿回复，谢谢！</h3>', 
			'<p>------------------------------------------------</p>',
			'<p><img src="http://10.10.10.93:8080/static/imgs/operations_sign.jpg"></p>', 
			'</body></html>')
		msg = MIMEText(''.join(msg),'html','utf-8')
		msg['From'] = self.mailfrom
		msg['To'] = mail_to
		msg['Subject'] = Header(subject,'utf-8')


		conn = smtplib.SMTP(self.mailserver)
		conn.sendmail(self.mailfrom, mail_to, msg.as_string())
		conn.close()




if __name__=="__main__":
	#sys.argv[1]:收件人列表(多个收件人以逗号分隔), sys.argv[2]:邮件主题 , sys.argv[3]：邮件正文内容
	obj = SendMail('127.0.0.1', 'operations')
	obj.mail(sys.argv[1], sys.argv[2], sys.argv[3])
