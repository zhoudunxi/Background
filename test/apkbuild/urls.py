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
from django.conf.urls import url
from apkbuild.apkbuild_view import APKRequest
from apkbuild.apkqueue_view import APKQueue
from apkbuild.apkqueue_view import Status_Queue
from apkbuild.apkqueue_detail_view import APKQueue_Detail

urlpatterns = [
	url(r'^apkrequest/$',APKRequest),
	url(r'^apkqueue/$',APKQueue),
	url(r'^apkqueue/qstatus$',Status_Queue),
	url(r'^apkqueue/queuedetail$',APKQueue_Detail),
]
