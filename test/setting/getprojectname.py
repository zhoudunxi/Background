# -*- coding: utf-8 -*-
from  project_manegement.models import project
from setting.models import user_with_project

def GetProjectName(userid):
	projectid_list = user_with_project.objects.filter(user_id=userid).values_list('project_id') #项目ID
	project_name = []
	for proje_li in projectid_list:
		try:
			project_data = project.objects.get(id=proje_li[0])
			project_name.append((project_data.project_name,project_data.id))
		except:
			print "select db error!!!!! for get project-objects ,from setting/getprojectname.py"
	return project_name

def AllProjectName():
	project_list = project.objects.all().values_list('project_name','id')
	project_name = []
	for pro_li in project_list:
		project_name.append(pro_li)
	return project_name
