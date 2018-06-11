        $(function(){
                $(".EditUser").click(function(){
                    var UserID = $(this).attr("user-id");//获取html中的变量
                    window.location.href="/setting/edituser?edituserid="+UserID;
                })

                $(".EditPassword").click(function(){
                    var UserID = $(this).attr("user-id");//获取html中的变量
                    window.location.href="/setting/editpassword?edituserid="+UserID;
                })

                $(".DeleteUser").click(function(){
                        var UserID = $(this).attr("user-id");//获取html中的变量
                        var UserName=$(this).attr("user-name");//获取html中的变量
                        if(window.confirm("警告！是否确认删除用户 "+UserName+" ?")){ //点击事件
                                window.location.href="/setting?deleteuserid="+UserID; //用同步的方式get到后端服务器
                        }
                })
     	})

