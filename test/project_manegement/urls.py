# -*- coding: utf-8 -*-
"""linux_govern URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import  url
from project_manegement.projectMAN_view import ADD_storage, ADD_project, EDIT_project, EDIT_storage

urlpatterns = [
	url(r'^addstorage/$',ADD_storage),
	url(r'^editstorage/$',EDIT_storage),
	url(r'^addproject/$',ADD_project),
	url(r'^editproject/$',EDIT_project),
]
