# -*- coding: utf-8 -*-
#分页
#导入数据库模型
import release.models
from project_manegement.models import project
from django.forms.models import model_to_dict ##django 将model转换为字典
from django.contrib.auth.models import User #django 认证用户表
import datetime

#current_page 当前页数，columns_table表显示列数，columns_page分页显示数, select_data查询到的是数据
def Paging(current_page, columns_table, columns_page, select_total):
	#	select_total = release.models.server_hardware.objects.order_by('-id').values_list('id')[0][0]#查找数据库中表记录总数
	remainder = select_total % columns_table #余数
	pages_num_total = select_total / columns_table #整除页数，省略余数,页面总数
	if pages_num_total >= 1 and remainder != 0: #如果非第一页，有余数，那么总页数加一
		pages_num_total += 1
	if pages_num_total == 0:
		pages_num_total += 1
	if current_page == 1 and pages_num_total == 1 and remainder != 0:#如果是第一页，总页数页是一页，同时有余数，修改数据显示数
		columns_table = remainder

	if current_page == pages_num_total and remainder != 0:#如果是最后一页，同时有余数，修改数据显示数
		columns_table = remainder

	pages_display_remainder = pages_num_total % columns_page #分页显示页数，余数
	pages_display_num = pages_num_total / columns_page #总分页数
	if pages_display_remainder != 0: #如果展示页有余数，展示页加一
		pages_display_num += 1
	if current_page == 1 and pages_num_total == 1 and pages_display_remainder != 0:#如果显示页数有余数，修改显示页
		columns_page = pages_display_num
	pages_end = current_page + columns_page - 1  #根据当前页数，计算出结束页面数
	if pages_num_total < columns_page: #如果总页数小于显示页数 
		current_page = 1
		pages_end = pages_num_total
	if current_page == pages_num_total:#如果是最后一页
		pages_end = current_page
	pag_list = []
	while (current_page <= pages_end):#分页列表
		if current_page > pages_num_total:#如果当前页大于页面总数，跳过本次循环
			current_page += 1
			continue
		pag_list.append(current_page)
		current_page += 1

	return (pag_list, pages_num_total, select_total ) #返回分页数据表列表，分页显示页列表，分页总数, 数据查询数据条数

