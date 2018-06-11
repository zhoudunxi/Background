#coding:UTF-8

import json, ConfigParser
from django.http import HttpResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from configures.Nginx import Nginx
from configures.forms import NginxForm


def _nginx(func):
    """
    A decorator for nginx.
    """
    def __wrapper(request):
        nginxform = NginxForm(request.POST)
        if nginxform.is_valid():
            instance = Nginx()
            result = func(instance, nginxform.cleaned_data)
            if result['status'] == 200:
                return HttpResponse(json.dumps({'status':'success', 'data':result['data']}))
            elif result['status'] == 416:
                return HttpResponse(json.dumps({'status':'failure', 'data':'no data'}))
        else:
            return HttpResponse(json.dumps({'status':'failure', 'data':'post data invalid'}))
    return __wrapper

@csrf_protect
@login_required
@_nginx
def nginxindex(instance, params):
    """
    Select all the nginx configure files from database.
    :params: params, dict.
    """
    return instance.index(params)

@csrf_protect
@login_required
@_nginx
def nginxwritecontent(instance, params):
    """
    Fetch the nginx configure file data and write database.
    :params: params, dict.
    """
    return instance.write_content(params)

@csrf_protect
@login_required
@_nginx
def nginxgetcontent(instance, params):
    """
    Get the nginx configures file content.
    :params: params, dict. 
    """
    return instance.get_content(params)
        
@csrf_protect
@login_required
@_nginx
def nginxsync(instance, params):
    """
    Sync the nginx configure file to the backend hosts.
    :params: params, dict.
    """
    return instance.sync(params)

@csrf_protect
@login_required
def nginxdownload(request):
    """
    Download the nginx configure file.
    Request method is 'GET'.
    :params: params, dict.
    """
    nginxform = PhpForm(request.GET)
    if nginxform.is_valid():
        instance = Nginx()
        result = instance.get_content(nginxform.cleaned_data)
        #Response 404 http code when the project id is nonexistent.
        if result['status'] == 416:
            return HttpResponse(status=404)
        #download
        filename = nginxform.cleaned_data['filename']
        response = StreamingHttpResponse(result['data'])
        response['Content-Type'] = 'text/file'
        response['Content-Disposition'] = 'attachment;filename=%s'%filename
        return response

@csrf_protect
@login_required
def nginxrollback(request):
    """
    Download the nginx configure file.
    Request method is 'GET'.
    :params: params, dict.
    """
    return {'status':200, 'data':'success'}

@csrf_protect
@login_required
def nginxdelete(request):
    """
    Download the nginx configure file.
    Request method is 'GET'.
    :params: params, dict.
    """
    return {'status':200, 'data':'success'}