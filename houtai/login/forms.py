# -*- coding: utf-8 -*-
from django import forms

class Login_Contact(forms.Form):
        username = forms.CharField(max_length=520,widget=forms.TextInput(attrs={'class':'form-control'}),label='')
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),label='')
