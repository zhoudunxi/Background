#coding=UTF-8
import logging, os
from configs import getconfig


#日志文件
logfile = getconfig('log', 'file')
try:
	os.stat(os.path.dirname(logfile))
except:
	os.makedirs(os.path.dirname(logfile))
#日志级别，大小关系为：CRITICAL > ERROR > WARNING > INFO > DEBUG。
loglevel = getconfig('log', 'level')

def log(level, content):
	if loglevel == "INTO" or loglevel == "info":
		LEVEL = logging.INFO
	elif loglevel == "WARNING" or loglevel == "warning":
		LEVEL = logging.WARNING
	elif loglevel == "ERROR" or loglevel == "error":
		LEVEL = logging.ERROR
	elif loglevel == "CRITICAL" or loglevel == "critical":
		LEVEL = logging.CRITICAL
	else:LEVEL = logging.DEBUG

	logging.basicConfig(level=LEVEL,
		format='%(asctime)s %(levelname)s %(message)s',
		datefmt='%d %b %Y %H:%M:%S',
		filename=logfile,
		filemode='a')

	if level == "info":
		logging.info(content)
	elif level == "warning":
		logging.warning(content)
	elif level == "error":
		logging.error(content)
	elif level == "critical":
		logging.critical(content)
	else:logging.debug(content)
