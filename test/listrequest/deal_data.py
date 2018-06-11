# -*- coding: utf-8 -*-
#导入数据库模型
import release.models
from project_manegement.models import project
from django.forms.models import model_to_dict ##django 将model转换为字典
from django.contrib.auth.models import User #django 认证用户表
import datetime
from django.db.models import Q #用于数据库or查询
from release.get_opsproject_user import ops_for_project_user



def deal_display_data(release_data):
    list_data = []
    countI = 0
    while  countI < len(release_data):
        data_from_db = model_to_dict(release_data[countI])
        try:
            data_from_db['project_id'] = project.objects.get(
                id=data_from_db['project_id']).project_name  # 根据项目id获取，项目名称
        except:
            data_from_db['project_id'] = '该项目已经被删除'
        description_data = data_from_db['description']
        data_from_db['description'] = description_data.split('\r\n')  # 格式化描述数据
        begin_CSTtime = release_data[countI].begin_time + datetime.timedelta(hours=+8)
        data_from_db['begin_time'] = begin_CSTtime.strftime('%Y-%m-%d %H:%M:%S')  # 转换成东八区时间
        try:
            data_from_db['last_user_id'] = User.objects.get(id=data_from_db['last_user_id']).last_name
        except:  # 如果有被删除的用户就pass
            data_from_db['last_user_id'] = '该用户已经被删除'
        if data_from_db['last_time'] != None:  # 如果取出表取出的数据不是空，转换时间
                last_CSTtime = release_data[countI].last_time + datetime.timedelta(hours=+8)
                data_from_db['last_time'] = last_CSTtime.strftime('%Y-%m-%d %H:%M:%S')
        data_from_db['ops_user_list'] = ops_for_project_user(data_from_db['id'])  # 获取项目运维, 根据上线id查找的

        list_data.append(data_from_db)
        countI += 1
    return list_data

#Q查询的字符拼接 说明： 字段名，列表
def or_select(table_field,str_list):
    orselect = ''
    for je_list in str_list:  # 字符拼接，Q() 加 | 是执行或查询，因为函数不接受字符作为参数，所以拼接完成后用eval()函数转换成元祖
        if len(str_list) == 1:
            orselect = '(Q(%s=%s))' % (table_field,je_list[0])
            break
        if je_list == str_list[0]:
            orselect += '(Q(%s=%s)|' % (table_field,je_list[0])
            continue
        if je_list == str_list[-1]:
            orselect += 'Q(%s=%s))' % (table_field,je_list[0])
            break
        orselect += 'Q(%s=%s)|' % (table_field,je_list[0])
    if orselect == '':
        orselect = 0
    else:
        orselect = eval(orselect)  # 将拼接好的字符转换成元祖，我们这里拼接的是元祖
    return orselect