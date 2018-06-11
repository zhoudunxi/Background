# -*- coding: utf-8 -*-
import requests, time
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import permission_required
__author__ = 'wch96'



####判断当前时间是否为节假日，
# 工作日对应结果为 0,
# 休息日对应结果为 1,
# 节假日对应的结果为 2；


class Is_duty(object):

    def __init__(self,url):
        self.__url = url

    def gettime(self):
        time_params = time.strftime("%Y%m%d", time.localtime())
        return time_params

    def request_api(self):
        try:
            code_res = requests.get(self.__url,params=dict(d=self.gettime()))
            ####如果正确返回则为正确返回的值 否则返回-1
            res_out = code_res.text if code_res.status_code == 200 else -1
            return res_out
        except Exception as e:
            return "requests is error"


# 请求方式 get    地址 http://localhost:8000/duty/
#@csrf_protect
#@permission_required('release.change_release',login_url='/login/')
def req_duty(request):
    if request.method == 'GET':
        res = Is_duty("http://tool.bitefu.net/jiari/")
        return HttpResponse(res.request_api())
