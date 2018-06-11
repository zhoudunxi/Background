# -*- coding: utf-8 -*-
#导入django表单模块
from django import forms
from project_manegement.models import project
#更新的表单
class Release_Form(forms.Form):
	#required=False, 表示可以为空,rows是高
	#projectname = forms.ChoiceField(label='项目',widget=forms.Select(attrs=pro2))
    description = forms.CharField(required=False,widget=forms.Textarea(attrs={'placeholder':'','class':'form-control input-sm','rows':'3'}),label='更新描述')
    filelist = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'','class':'form-control input-sm','rows':'20'}),label='文件列表')

class DBA_Release_Form(forms.Form):
    sql_statement = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': '', 'class': 'form-control input-sm', 'rows': '5'}), label='SQL语句')
