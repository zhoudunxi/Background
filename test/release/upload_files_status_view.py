# -*- coding: utf-8 -*-
#修改值班状态，现在用于请假
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from release.models import ops_release

@csrf_protect
@login_required(login_url='/login/')
#
def upload_files_status(request):
    if request.method == "POST":
        release_id = request.POST.get('release_id')
        upload_file_status = ops_release.objects.get(request_id=release_id).upload_file_status
        upload_file_status = eval(upload_file_status)
        return HttpResponse(json.dumps(upload_file_status))
    else:
        return HttpResponse('fuck man')