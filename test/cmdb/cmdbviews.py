# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseRedirect
from django.contrib.sessions.models import Session
from release.obtain_nav import header_left_nav
from models import cmdbmanage, cmdbgroup
import uuid, json, random
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
# Create your views here.

#管理cmdb函数
Group = {
    1:"日志",
    2:"活动",
    3:"套掌柜接口",
    4:"淘集集API-cli-pay-fbsapi",
    5:"淘集集后台",
    6:"淘集集静态资源",
    7:"物流",
    8:"短信",
    9:"闪电发",
    10:"闪电发静态资源",
    11:"闪电降-M站-后台活动",
    12:"闪电降接口",
    13:"闪电降静态资源",
    14:"快选接口",
    15:"快选后台",
    16:"快选活动",
    17:"快选后台静态资源",
    18:"快选发",
    19:"快选发静态资源",
}
Env = {
    1000:"生产",
    1001:"灰度",
    1002:"预发布",
    1003:"测试",
}

@csrf_exempt
@login_required(login_url='/login/')
def Cmdb(request):
    if not request.user.is_authenticated(): #校验是否认证，如果没有认证跳转到登陆页面
        return HttpResponseRedirect('/login/?next=%s' % request.path)
    session_key = request.session.session_key #获取sessionid
    userid = Session.objects.get(pk=session_key).get_decoded()['_auth_user_id'] #更加sessionid查找出userid，根据userid做权限控制
    left_return = header_left_nav('资产管理',userid) #调用模块，获取返回左导航元组数据
    allcmdb = cmdbmanage.objects.all()
    if request.method == 'GET':
        #page = request.GET.get("page") 另外一种分页效果 比如请求 http://localhost:8000/cmdb/?page=12
        #print(page)
        selectcmdb = cmdbgroup.objects.all()
        #return render_to_response("cmdb.html", {'left_nav': left_return, "res_info": allcmdb,"select_info":selectcmdb})
        return render(request,"cmdb.html",
                                  {'left_nav': left_return, "res_info": allcmdb, "select_info": selectcmdb})
    else:
        uuidnum = str(uuid.uuid1()).split("-")[0]
        serverip = request.POST.get("serverip")
        memory = request.POST.get("memory")
        cpu = request.POST.get("cpu")
        release = request.POST.get("release")
        complay = request.POST.get("complay")
        apisoft = request.POST.get("apisoft")
        try:
            group = request.POST.getlist("group")
        except:
            group = int(request.POST.get("group"))
        group = [ip.progroup for ip in cmdbgroup.objects.filter(id__in = group)]
        group = ",".join(group).split("||||")
        env = Env[int(request.POST.get("env"))]
        Uuid = request.POST.get("id")
        if len(str(serverip).split("|")) > 1:
            cmdbmanage.objects.filter(uid = Uuid).update(server_ip = serverip.split("|")[0].strip() or "空", server_mem = memory or "空", server_cpu = cpu or "空", server_system = release or "空", \
            server_position = complay or "空", server_service = apisoft or "空", group = group[0] or "空", env = env or "空")
        else:
            cmdbmanage.objects.create(uid = uuidnum, server_ip = serverip or "空", server_mem = memory or "空", server_cpu = cpu or "空", server_system = release or "空", \
            server_position = complay or "空", server_service = apisoft or "空", group = group[0] or "空", env = env or "空")
        allcmdb = cmdbmanage.objects.all()
        selectcmdb = cmdbgroup.objects.all()
        #return render_to_response('cmdb.html',{'left_nav': left_return, "res_info": allcmdb,"select_info":selectcmdb})
        return render(request,'cmdb.html',
                                  {'left_nav': left_return, "res_info": allcmdb, "select_info": selectcmdb})


#删除cmdb函数
@csrf_exempt
@login_required(login_url='/login/')
def del_cmdb(request):
    if not request.user.is_authenticated(): #校验是否认证，如果没有认证跳转到登陆页面
        return HttpResponseRedirect('/login/?next=%s' % request.path)
    session_key = request.session.session_key #获取sessionid
    userid = Session.objects.get(pk=session_key).get_decoded()['_auth_user_id'] #更加sessionid查找出userid，根据userid做权限控制
    left_return = header_left_nav('资产管理',userid) #调用模块，获取返回左导航元组数据
    uuidnum = request.POST.get("num")
    cmdbmanage.objects.filter(uid = uuidnum).delete()
    allcmdb = cmdbmanage.objects.all()
    #return render_to_response('cmdb.html',{'left_nav': left_return, "res_info": allcmdb})
    return render(request,'cmdb.html', {'left_nav': left_return, "res_info": allcmdb})

#提供接口函数账户和密码   外部请求接口 http://localhost:8000/cmdb_api/?secret_KEY=4cc0a440319d11e8a3342816ad1003e6&secret_ID=sdjj
@csrf_exempt
@login_required(login_url='/login/')
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
        #print(data)
        result = {"status": "Success",
              "info": "welcome to sdjj",
              "datanum": len(data),
              "data": data
    }
        return HttpResponse(json.dumps(result))

#http://localhost:8000/cmdb_api_group/?group=all&env=all
@csrf_exempt
@login_required(login_url='/login/')
def Cmdb_api_group(request):
    if request.GET.get("group") == "all" and request.GET.get("env") == "all":
        data = cmdbgroup.objects.all()
        Group = {}
        for i in data:
            Group[i.id] = i.progroup
        Env.update(Group)
        return HttpResponse(json.dumps(Env))
    else:
        try:
            num1 = int(request.GET.get("group"))
            print(num1)
            env = int(request.GET.get("env"))
            ########开始得出id in那个字段的值
            data = cmdbgroup.objects.filter(id = num1)
            #print(data)
            dataall = []
            for i in data:
                datas = i.progroup
            for ii in cmdbmanage.objects.all():
                #print(ii.group,ii.server_ip)
                if datas in ii.group.split(","):
                    dataall.append(ii)
            #dataall = cmdbmanage.objects.filter(group = datas,env=Env[env])
            data = dict(server_ip=[IP.server_ip for IP in dataall])
            return HttpResponse(json.dumps(data))
        except:
            return HttpResponse(json.dumps(dict(status="ERROR",data="请求格式错误")))

@csrf_exempt
@login_required(login_url='/login/')
def Cmdb_Group(request):
    if not request.user.is_authenticated(): #校验是否认证，如果没有认证跳转到登陆页面
        return HttpResponseRedirect('/login/?next=%s' % request.path)
    session_key = request.session.session_key #获取sessionid
    userid = Session.objects.get(pk=session_key).get_decoded()['_auth_user_id'] #更加sessionid查找出userid，根据userid做权限控制
    left_return = header_left_nav('资产管理',userid) #调用模块，获取返回左导航元组数据
    try:
        proname = request.POST.get("progroup")
        while True:
            ID = random.randint(0,99)
            if cmdbgroup.objects.filter(id = ID):
                pass
            else:
                break
        cmdbgroup.objects.create(id = ID, optionid=proname, progroup = proname or "空")
        allcmdb = cmdbmanage.objects.all()
        selectcmdb = cmdbgroup.objects.all()
        #return render_to_response('cmdb.html',{'left_nav': left_return, "res_info": allcmdb, "select_info": selectcmdb})
        return render(request,'cmdb.html',
                                  {'left_nav': left_return, "res_info": allcmdb, "select_info": selectcmdb})
    except:
        return HttpResponseRedirect('/cmdb')

@csrf_exempt
def Cmdb_select(request):
    if not request.user.is_authenticated(): #校验是否认证，如果没有认证跳转到登陆页面
        return HttpResponseRedirect('/login/?next=%s' % request.path)
    session_key = request.session.session_key #获取sessionid
    userid = Session.objects.get(pk=session_key).get_decoded()['_auth_user_id'] #更加sessionid查找出userid，根据userid做权限控制
    left_return = header_left_nav('资产管理',userid) #调用模块，获取返回左导航元组数据
    try:
        if request.method == "POST":
            selectid1 = request.POST.get("num1") if request.POST.get("num1") != "未分类" else "空"
            selectid2 = request.POST.get("num2")
            #print(selectid1,selectid2)
            #print("ook")
            return HttpResponse("/cmdb/Cmdb_select/?xiangmufenzu=%s&jiqizhuangtai=%s" %(selectid1,selectid2))
        else:
            selectid1 = request.GET.get("xiangmufenzu")
            selectid2 = request.GET.get("jiqizhuangtai")
            if selectid1 == "全部" and selectid2 == "全部":
                allcmdb = cmdbmanage.objects.all()
            elif selectid1 == "全部" and selectid2 != "全部":
                allcmdb = cmdbmanage.objects.filter(status=selectid2)
            elif selectid1 not in ["全部","空"] and selectid2 == "全部":
                allcmdb = cmdbmanage.objects.filter(~Q(group="空"))
            elif selectid1 not in ["全部","空"] and selectid2 != "全部":
                allcmdb = cmdbmanage.objects.filter(~Q(group="空"),status=selectid2)
            elif selectid1 == "空" and selectid2 != "全部":
                allcmdb = cmdbmanage.objects.filter(group=selectid1,status=selectid2)
            elif selectid1 == "空" and selectid2 == "全部":
                allcmdb = cmdbmanage.objects.filter(group=selectid1)
            else:
                allcmdb = cmdbmanage.objects.filter(group=selectid1,status=selectid2)
            selectcmdb = cmdbgroup.objects.all()
            #print(selectid1,selectid2)
            #print("ok")
            return render_to_response('cmdb.html',{'left_nav': left_return, "res_info": allcmdb, "select_info": selectcmdb})
    except:
        return HttpResponse("ERROR 连续管理员")


def Cmdb_group(num1, num2):
    if num1 == "all" and num2 == "all":
        data = cmdbgroup.objects.all()
        Group = {}
        for i in data:
            Group[i.id] = i.progroup
        Env.update(Group)
        return json.dumps(Env)
    else:
        try:
            num1 = num1
            #env = int(request.GET.get("env"))
            ########开始得出id in那个字段的值
            data = cmdbgroup.objects.filter(id = num1)
            #print(data)
            dataall = []
            datas = ''
            for i in data:
                datas = i.progroup
            for ii in cmdbmanage.objects.all():
                #print(ii.group,ii.server_ip)
                if datas in ii.group.split(","):
                    dataall.append(ii)
            #dataall = cmdbmanage.objects.filter(group = datas,env=Env[env])
            data = dict(server_ip=[IP.server_ip for IP in dataall])
            return json.dumps(data)
        except:
            return json.dumps(dict(status="ERROR",data="请求格式错误"))
