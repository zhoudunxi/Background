# -*- coding: utf-8 -*-
import settings
#from django.conf.urls import patterns, include, url
from django.conf.urls import include, url
from django.views import static

from django.contrib import admin
admin.autodiscover()

from login.login_views import Login, Logout
from release.release_view import Release
from listrequest.listRE_view import REList
from project_manegement.projectMAN_view import Project_mana
from apkbuild.apkbuild_view import APKBuild
from setting.setting_view import Setting
from apphelp.help_view import Help
from cmdb.cmdbviews import Cmdb, del_cmdb, Cmdb_Group
from api.duty import req_duty
from api.cmdb_api import Cmdb_api
from cmdb.cmdbviews import Cmdb_api_group, Cmdb_select
#urlpatterns = patterns('',
urlpatterns = [
    # Examples:
    # url(r'^$', 'release_sdjj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	#url(r'^admin/', include(admin.site.urls)),
	url( r'^static/(?P<path>.*)$',static.serve,{ 'document_root': 'settings.STATICFILES_DIRS'}),
	url(r'^login/$',Login),
	url(r'^logout/$',Logout),
	url(r'^release/$',Release),
	#url(r'^release/request/$',Request),
	url(r'^release/',include('release.urls')),
	url(r'^requestlist/$',REList),
	url(r'^projectmanegement/$',Project_mana),
	url(r'^projectmanegement/',include('project_manegement.urls')),
	url(r'^apkupdate/$',APKBuild),
	url(r'^apkupdate/',include('apkbuild.urls')),
	url(r'^setting/$',Setting),
	url(r'^setting/',include('setting.urls')),
	url(r'^help/$',Help),
	url(r'^cmdb/$',Cmdb),
	url(r'^cmdb/group$',Cmdb_Group),
	url(r'^cmdb/Cmdb_select/',Cmdb_select),
	url(r'^del_cmdb/$',del_cmdb),
	url(r'^cmdb_api/$',Cmdb_api),
	url(r'^duty/$',req_duty),
	url(r'^cmdb_api_group/$',Cmdb_api_group),
	url(r'^configures/',include('api.urls')),
    url(r'^configures/php/',include('configures.urls')),
]
