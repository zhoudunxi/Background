# -*- coding: utf-8 -*-
#导入django表单模块
from django import forms
#导入仓库模板，用户读取仓库名
from project_manegement.models import storage
from public.get_cmdb_info import get_group_hosts
import json

#仓库表单
class Storage_Form(forms.Form):
    name = forms.CharField(max_length=500,widget=forms.TextInput(attrs={'placeholder':'*必填','class':'form-control input-sm col-md-4'}),label='仓库名称')
    #required=False 表示可选项，表单不会抛出错误
    description = forms.CharField(required=False,max_length=2048,widget=forms.Textarea(attrs={'placeholder':'','class':'form-control input-sm'}),label='仓库描述')
    back_path = forms.CharField(max_length=999,widget=forms.TextInput(attrs={'placeholder':'*例:/data/backup','class':'form-control input-sm'}),label='备份目录')
    git_path = forms.CharField(max_length=999,widget=forms.TextInput(attrs={'placeholder':'*例:/data/git/','class':'form-control input-sm'}),label='git目录')
    staging_path = forms.CharField(max_length=999,widget=forms.TextInput(attrs={'placeholder':'*例:/data/stagin','class':'form-control input-sm'}),label='镜像目录')
    #sync_script = forms.CharField(max_length=999,widget=forms.TextInput(attrs={'placeholder':'*例:/data/online/sync.sh','class':'form-control input-sm'}),label='同步脚本')
    branch_name = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'placeholder':'*master或者test...','class':'form-control input-sm'}),label='代码分支')
    enable_pre_env = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'placeholder':'*true 或者 false','class':'form-control input-sm'}),label='是否预发布')
    staging_path_for_pre = forms.CharField(required=False,max_length=999,widget=forms.TextInput(attrs={'placeholder':'','class':'form-control input-sm'}),label='预发布镜像目录')
    #sync_script_for_pre = forms.CharField(required=False,max_length=999,widget=forms.TextInput(attrs={'placeholder':'','class':'form-control input-sm'}),label='预发布同步脚本')


class Storage_Edit_Form(forms.Form):
    #required=False 表示可选项，表单不会抛出错误
    description = forms.CharField(required=False,max_length=2048,widget=forms.Textarea(attrs={'placeholder':'','class':'form-control input-sm'}),label='仓库描述')
    back_path = forms.CharField(max_length=999,widget=forms.TextInput(attrs={'placeholder':'*例:/data/backup','class':'form-control input-sm'}),label='备份目录')
    git_path = forms.CharField(max_length=999,widget=forms.TextInput(attrs={'placeholder':'*例:/data/git/','class':'form-control input-sm'}),label='git目录')
    staging_path = forms.CharField(max_length=999,widget=forms.TextInput(attrs={'placeholder':'*例:/data/stagin','class':'form-control input-sm'}),label='镜像目录')
    sync_script = forms.CharField(max_length=999,widget=forms.TextInput(attrs={'placeholder':'*例:/data/online/sync.sh','class':'form-control input-sm'}),label='同步脚本')
    branch_name = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'placeholder':'*master或者test...','class':'form-control input-sm'}),label='代码分支')
    enable_pre_env = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'placeholder':'*true 或者 false','class':'form-control input-sm'}),label='是否预发布')
    staging_path_for_pre = forms.CharField(required=False,max_length=999,widget=forms.TextInput(attrs={'placeholder':'','class':'form-control input-sm'}),label='预发布镜像目录')
    sync_script_for_pre = forms.CharField(required=False,max_length=999,widget=forms.TextInput(attrs={'placeholder':'','class':'form-control input-sm'}),label='预发布同步脚本')


class Project_Form(forms.Form):
    #project_name = forms.CharField(max_length=500,widget=forms.TextInput(attrs={'placeholder':'*必填','class':'form-control input-md','style':'width:200px'}),label='项目名称')
    #project_name = forms.ChoiceField(choices=group_name,required=False,widget=forms.Select(attrs={'class':'form-control input-md','style':'width:200px'}),label='项目名称')
    #storage_id = forms.ChoiceField(choices=storage_info,required=False,widget=forms.Select(attrs={'class':'form-control input-md','style':'width:200px'}),label='请选择仓库')
    storage_id = forms.ChoiceField(required=False,widget=forms.Select(attrs={'class':'form-control input-md','style':'width:200px'}),label='请选择仓库')
    project_label = forms.CharField(max_length=30,required=False,widget=forms.TextInput(attrs={'placeholder':'例如:web 可以为空','class':'form-control input-md','style':'width:200px'}),label='忽略目录')
    remote_path = forms.CharField(max_length=999,widget=forms.TextInput(attrs={'placeholder':'*例如:/data/shandjjroot','class':'form-control input-md'}),label='远程目录')
    pre_remote_path = forms.CharField(required=False,max_length=999,widget=forms.TextInput(attrs={'placeholder':'例如:/data/shandjjroot','class':'form-control input-md'}),label='预发布远程目录')
    project_description = forms.CharField(required=False,max_length=2048,widget=forms.Textarea(attrs={'placeholder':'','class':'form-control input-md'}),label='项目描述')
    def __init__(self, *args, **kwargs):  # 自定义__init__
        super(Project_Form, self).__init__(*args, **kwargs) # 调用父类的__init__
        self.fields['storage_id'].choices = storage.objects.all().values_list('id','name')  # 为字段t2c的choices赋值

