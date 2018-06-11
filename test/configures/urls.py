#coding:UTF-8


from django.conf.urls import url
from configures.views import configures,getgroup,getpage

urlpatterns = [
    url(r'^$', configures),
    url(r'^getgroup/$', getgroup),
    url(r'^getpage/$', getpage),
]

from django.conf.urls import url

