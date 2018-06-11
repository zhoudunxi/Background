#/usr/bin/python
#encoding=utf8
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseRedirect
from django.contrib.sessions.models import Session
from release.obtain_nav import header_left_nav
#from models import cmdbmanage, cmdbgroup
from cmdb.models import cmdbgroup
import uuid, json, random
from django.views.decorators.csrf import csrf_exempt
# Create your views here

def configures(request):
    if not request.user.is_authenticated(): #校验是否认证，如果没有认证跳转到登陆页面
        return HttpResponseRedirect('/login/?next=%s' % request.path)
    session_key = request.session.session_key #获取sessionid
    userid = Session.objects.get(pk=session_key).get_decoded()['_auth_user_id'] #更加sessionid查找出userid，根据userid做权限控制
    left_return = header_left_nav('配置管理',userid) #调用模块，获取返回左导航元组数据.
    return  render(request,"configures.html",
                                  {'left_nav': left_return})


def getgroup(request):
    alldata = cmdbgroup.objects.all()
    tmplist = [[i.id,i.optionid] for i in alldata]
    #print(tmplist)
    return HttpResponse(json.dumps(tmplist))


def getpage(request):
    data = {
        "totalPage": 10,
        "totalSize": 300,
        "data": []
    }
    return HttpResponse(json.dumps(data))