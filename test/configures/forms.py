#coding=UTF-8

from django import forms


class PhpForm(forms.Form):
    projectid = forms.IntegerField(required=False)
    filename = forms.CharField(max_length=30, required=False)
    #The key for a option of the configure file.
    option = forms.CharField(max_length=30, required=False)
    #The value for a option of the configure file.
    value = forms.CharField(max_length=256, required=False)
    content = forms.CharField(max_length=16777215, required=False)
    #Page number.
    pageid = forms.IntegerField(required=False)
    #Numbers in per page.
    perpage = forms.IntegerField(required=False)
    #Running environment.
    env = forms.IntegerField(required=False)

class NginxForm(forms.Form):
    projectid = forms.IntegerField(required=False)
    filename = forms.CharField(max_length=30, required=False)
    content = forms.CharField(max_length=16777215, required=False)
    #Page number.
    pageid = forms.IntegerField(required=False)
    #Numbers in per page.
    perpage = forms.IntegerField(required=False)
    #Running environment.
    env = forms.IntegerField(required=False)