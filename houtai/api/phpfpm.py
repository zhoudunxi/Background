#coding:UTF-8

import json, ConfigParser
from django.http import HttpResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from configures.Phpfpm import Phpfpm
from configures.forms import PhpForm


def _phpfpm(func):
    """
    A decorator for phpfpm.
    """
    def __wrapper(request):
        phpform = PhpForm(request.POST)
        if phpform.is_valid():
            instance = Phpfpm()
            result = func(instance, phpform.cleaned_data)
            if result['status'] == 200:
                return HttpResponse(json.dumps({'status':'success', 'data':result['data']}))
            elif result['status'] == 416:
                return HttpResponse(json.dumps({'status':'failure', 'data':'no data'}))
            elif result['status'] == 409:
                return HttpResponse(json.dumps({'status':'failure', 'data':'conflict'}))
        else:
            return HttpResponse(json.dumps({'status':'failure', 'data':'post data invalid'}))
    return __wrapper

#@csrf_protect
@csrf_exempt
@login_required
@_phpfpm
def phpfpmindex(instance, params):
    """
    Select all the php-fpm configure files from database.
    :params: params, dict.
        pageid, int, page number. Default 1.
        perpage, int, how many records are in per page. Default 10.
    """
    return instance.index(params)

#@csrf_protect
@csrf_exempt
@login_required
@_phpfpm
def phpfpmupload(instance, params):
    """
    Fetch the php-fpm configure file data and write database.
    :params: params, dict.
        projectid, int, project id.
        filename, string, the name of the configure file.
        content, string, the content of the configure file.
        env, int, the running environment.
    """
    return instance.upload(params)

#@csrf_protect
@csrf_exempt
@login_required
@_phpfpm
def phpfpmgetcontent(instance, params):
    """
    Get the php-fpm configures file content.
    :params: params, dict. 
        projectid, int, project id.
        env, int, the running environment.
    """
    return instance.get_content(params)
        
#@csrf_protect
@csrf_exempt
@login_required
@_phpfpm
def phpfpmgetoptions(instance, params):
    """
    Get all sections of the php-fpm configures file. 
    :params: params, dict.
        projectid, int, project id.
        env, int, the running environment.
    """
    return instance.get_options(params)

#@csrf_protect
@csrf_exempt
@login_required
@_phpfpm
def phpfpmgetvalue(instance, params):
    """
    Get the value of an option in a section.
    :params: params, dict. Include the value of a 'option'.
        projectid, int, project id.
        env, int, the running environment.
        option, string, an option in the configure file.
    """
    return instance.get_value(params)

#@csrf_protect
@csrf_exempt
@login_required
@_phpfpm
def phpfpmsetvalue(instance, params):
    """
    Set the value of an option in a section.
    :params: params, dict. Include the value of a 'option'.
        projectid, int, project id.
        env, int, the running environment.
        option, string, an option in the configure file.
        value, string, the value with the option.
    """
    return instance.set_value(params)

#@csrf_exempt
@csrf_exempt
@login_required
@_phpfpm
def phpfpmsync(instance, params):
    """
    Sync the php-fpm configure file to the backend hosts.
    :params: params, dict.
        projectid, int, project id.
        env, int, the running environment.
    """
    return instance.sync(params)

@csrf_protect
@login_required
def phpfpmdownload(request):
    """
    Download the php-fpm configure file.
    Request method is 'GET'.
    :params: params, dict.
        projectid, int, project id.
        env, int, the running environment.
    """
    phpform = PhpForm(request.GET)
    if phpform.is_valid():
        instance = Phpfpm()
        result = instance.get_content(phpform.cleaned_data)
        #Response 404 http code when the project id is nonexistent.
        if result['status'] == 416:
            return HttpResponse(status=404)
        #download
        filename = phpform.cleaned_data['filename']
        response = StreamingHttpResponse(result['data'])
        response['Content-Type'] = 'text/file'
        response['Content-Disposition'] = 'attachment;filename=%s'%filename
        return response


@csrf_protect
@login_required
@_phpfpm
def phpfpmrollback(instance, params):
    """
    Rollback for the latest sync.
    :params: params, dict.
        projectid, int, project id.
        env, int, the running environment.
    """
    return instance.rollback(params)

#@csrf_protect
@csrf_exempt
@login_required
@_phpfpm
def phpfpmdelete(instance, params):
    """
    Delete a php-fpm configure file.
    :params: params, dict.
        projectid, int, project id.
        env, int, the running environment.
    """
    return instance.delete(params)