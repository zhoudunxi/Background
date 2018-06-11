#!/bin/env python
#coding: utf-8
#读取配置文件
import os, sys
import ConfigParser

def Project_Info():
	#config_file = '/data/release_sdjj' + os.sep + 'apkbuild' + os.sep + 'configs' + os.sep + 'ProjectName.conf' 
	config_file = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'configs' + os.sep + 'ProjectName.conf' 
	conf = ConfigParser.SafeConfigParser()
	conf_temp = conf.read(config_file)
	return_list = []
	project_sections = conf.sections() #项目名称
	#return_list.append(project_sections)
	list_chinese = []
	list_version = []
	for section in project_sections:
		project_options = conf.options(section) #根据项目名称获取key
		for option in project_options:
			if option == 'version':
				ver_L = (section,conf.get(section,option).split('|'))
				list_version.append(ver_L)
			else:
				ver_L = (section,conf.get(section,option).split('|'))
				list_chinese.append(ver_L)
	return_list.append(list_chinese)
	return_list.append(list_version)
	return return_list	

def Get_CN_Name(section):
	#config_file = '/data/release_sdjj' + os.sep + 'apkbuild' + os.sep + 'configs' + os.sep + 'ProjectName.conf'
	config_file = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'configs' + os.sep + 'ProjectName.conf'
	conf = ConfigParser.SafeConfigParser()
	conf_temp = conf.read(config_file)
	return conf.get(section,'chinese_name')
	

