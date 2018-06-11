# -*- coding: utf-8 -*-
#修改值班状态，现在用于请假
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from setting.models import ops_duty


@csrf_protect
@login_required(login_url='/login/')
#POST参数userid operation ，operation的值只能是True或者False
def duty_operation(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        user_operation = request.POST.get('operation')
        duty_from_db = ops_duty.objects.get(user_id=userid)
        return_dist = {}
        return_dist['duty_return'] = {}
        return_dist['duty_return']['userid'] = userid
        if user_operation != duty_from_db.duty_status:
            if duty_from_db.duty_status:
                duty_from_db.duty_status = False
                duty_from_db.save()
                return_dist['duty_return']['status'] = 'success'
            else:
                duty_from_db.duty_status = True
                duty_from_db.save()
                return_dist['duty_return']['status'] = 'success'
        else:
            return_dist['duty_return']['status'] = 'The current state does not need to be modified'
    return HttpResponse(json.dumps(return_dist))
            #{'duty_return':{'userid':'1','status':'success'}}
