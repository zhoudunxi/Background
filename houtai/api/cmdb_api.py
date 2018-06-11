#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sessions.models import Session
from release.obtain_nav import header_left_nav
from cmdb.models import cmdbmanage
import uuid, json
#提供接口函数账户和密码   外部请求接口 http://localhost:8000/cmdb_api/?secret_KEY=4cc0a440319d11e8a3342816ad1003e6&secret_ID=sdjj
def Cmdb_api(request):
    secret_KEY = u"4cc0a440319d11e8a3342816ad1003e6"
    secret_ID = u"sdjj"
    if request.GET.get("secret_ID") != secret_ID or request.GET.get("secret_KEY") != secret_KEY:
        data = {}
        result = {"status": "Error",
                  "info": "secret_KEY or secret_ID are wrong",
                  "datanum": len(data),
                  "data": data
        }
        return HttpResponse(json.dumps(result))
    else:
        dataall = cmdbmanage.objects.all()
        data = [({"server_id": i.uid,"server_ip": i.server_ip, "server_mem": i.server_mem, "server_cpu": i.server_cpu, "server_system": i.server_system, \
                 "server_position": i.server_position, "server_service": i.server_service, "group": i.group}) for i in dataall]
        print(data)
        result = {"status": "Success",
              "info": "welcome to sdjj",
              "datanum": len(data),
              "data": data
    }
        return HttpResponse(json.dumps(result))
