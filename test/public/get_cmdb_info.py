# -*- coding: utf-8 -*-
from public.configs import getconfig
import urllib2, json
from cmdb.cmdbviews import Cmdb_group

#获取cmdb单个项目名，现在已经废弃，因为uwsgi无法内部调用
def get_group_hosts(group,env):
    cmdb_host = getconfig('cmdbserver','cmdb_host')
    cmdb_port = getconfig('cmdbserver','cmdb_port')
    urldata = urllib2.urlopen('http://%s:%s/cmdb_api_group/?group=%s&env=%s' %(cmdb_host, cmdb_port, group, env))
    #return_data = urldata.read()
    return urldata.read()

#获取cmdb所有组名
def deal_group():
    #dump_json = json.dumps(get_group_hosts('all','all'))
    group_name = json.loads(Cmdb_group('all','all'))
    return_data = []
    for key,value in group_name.items():
        return_data.append((key,value))
    return return_data
