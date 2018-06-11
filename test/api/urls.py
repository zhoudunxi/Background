#coding:UTF-8

from django.conf.urls import url
from phpfpm import *
from nginx import *


urlpatterns = [
	url(r'^api/phpfpm/index/$', phpfpmindex),
	url(r'^api/phpfpm/upload/$', phpfpmupload),
	url(r'^api/phpfpm/getcontent/$', phpfpmgetcontent),
	url(r'^api/phpfpm/getoptions/$', phpfpmgetoptions),
	url(r'^api/phpfpm/getvalue/$', phpfpmgetvalue),
	url(r'^api/phpfpm/setvalue/$', phpfpmsetvalue),
	url(r'^api/phpfpm/sync/$', phpfpmsync),
	url(r'^api/phpfpm/rollback/$', phpfpmrollback),
	url(r'^api/phpfpm/download/$', phpfpmdownload),
	url(r'^api/phpfpm/delete/$', phpfpmdelete),
	url(r'^api/nginx/index/$', nginxindex),
	url(r'^api/nginx/upload/$', nginxwritecontent),
	url(r'^api/nginx/getcontent/$', nginxgetcontent),
	url(r'^api/nginx/sync/$', nginxsync),
	url(r'^api/nginx/rollback/$', nginxrollback),
	url(r'^api/nginx/delete/$', nginxdelete),
]