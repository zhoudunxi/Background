                var addstatus=$('[name="addstatus"]').val();
                if(addstatus=="success")alert("添加用户成功！");
                if(addstatus=="passwdERROE")alert("注意！你输入的两次密码不一致！重新来过吧！");

                var editstatus=$('[name="editstatus"]').val();
                if(editstatus=="success"){
                    alert("编辑用户成功！");
                    window.location.href="/setting/";};


                var editpassword=$('[name="editpwd_status"]').val();
                var staff=$('[name="staff"]').val();
                if(editpassword=="success")
                    {alert("密码修改成功！")
                    if (staff == 'True'){
                        window.location.href="/setting/";}
                    else{
                        window.location.href="/login/"}
                };
                if(editpassword=="passwdERROE")alert("注意！你输入的两次密码不一致！重新来过吧！");
