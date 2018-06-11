# -*- coding: utf-8 -*-
#django http模块
from django.contrib.auth.models import User

def user_edit_pwd(edituserid,password,trypassword):
    if trypassword == password:
        from_db = User.objects.get(id=edituserid)
        from_db.set_password(trypassword)
        from_db.save()
        return_data = 'success'
    else:
        return_data = 'passwdERROE'
    return return_data