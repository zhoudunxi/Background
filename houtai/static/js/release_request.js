        $(function(){
                $(".carry_sql").click(function(){
                        if(window.confirm("SQL已经执行完成?")){ //点击事件
                                var reID=$(this).attr("RequestID") //获取页面中的变量，这是ID
                                var CSRF403=$('[name="csrfmiddlewaretoken"]').val(); //获取name为csrf......的value
                                var User_ID=$('[name="user_id"]').val(); //获取name为user_id的value,操作者的id
                                var $formpre=$("<form action='/release/request/' method='post'></form>");
                                $formpre.append($("<input type='hidden' name='csrfmiddlewaretoken' value="+CSRF403+" />"));
                                $formpre.append($("<input type='hidden' name='user_id' value="+User_ID+" />"));
                                $formpre.append($("<input type='hidden' name='doing' value='carry_sql'/>"));
                                $formpre.append($("<input type='hidden' name='RequestID' value="+reID+" />"));
                                $("body").append($formpre);
                                $formpre.submit();
                        }
                })
        })

        $(function(){
                $(".prepare").click(function(){
                        if(window.confirm("更新到预发布?")){ //点击事件
                                var reID=$(this).attr("RequestID") //获取页面中的变量，这是ID
                                var CSRF403=$('[name="csrfmiddlewaretoken"]').val(); //获取name为csrf......的value
                                var User_ID=$('[name="user_id"]').val(); //获取name为user_id的value,操作者的id
                                var $formpre=$("<form action='/release/request/' method='post'></form>");
                                $formpre.append($("<input type='hidden' name='csrfmiddlewaretoken' value="+CSRF403+" />")); 
                                $formpre.append($("<input type='hidden' name='user_id' value="+User_ID+" />")); 
                                $formpre.append($("<input type='hidden' name='doing' value='prepare'/>")); 
                                $formpre.append($("<input type='hidden' name='RequestID' value="+reID+" />"));
                                $("body").append($formpre);
                                $formpre.submit(); 
                        }
                })
        })

               $(function(){
                $(".dev_tested").click(function(){
                        if(window.confirm("预发布测试已经完成?")){ //点击事件
                                var reID=$(this).attr("RequestID") //获取页面中的变量，这是ID
                                var CSRF403=$('[name="csrfmiddlewaretoken"]').val(); //获取name为csrf......的value
                                var User_ID=$('[name="user_id"]').val(); //获取name为user_id的value,操作者的id
                                var $formpre=$("<form action='/release/request/' method='post'></form>");
                                $formpre.append($("<input type='hidden' name='csrfmiddlewaretoken' value="+CSRF403+" />"));
                                $formpre.append($("<input type='hidden' name='user_id' value="+User_ID+" />"));
                                $formpre.append($("<input type='hidden' name='doing' value='dev_tested'/>"));
                                $formpre.append($("<input type='hidden' name='RequestID' value="+reID+" />"));
                                $("body").append($formpre);
                                $formpre.submit();
                        }
                })
        })

        $(function(){
                $(".online").click(function(){
                        if(window.confirm("确定，更新到正式?")){ //点击事件
                                var reID=$(this).attr("RequestID") //获取页面中的变量，这是ID
                                var CSRF403=$('[name="csrfmiddlewaretoken"]').val(); //获取name为csrf......的value
                                var User_ID=$('[name="user_id"]').val(); //获取name为user_id的value,操作者的id
                                //window.location.href="/release/management-server/?pages-delete-id="+hardwareId; //用同步的方式get到后端服务器
                                var $formpre=$("<form action='/release/request/' method='post'></form>");
                                $formpre.append($("<input type='hidden' name='csrfmiddlewaretoken' value="+CSRF403+" />")); 
                                $formpre.append($("<input type='hidden' name='user_id' value="+User_ID+" />")); 
                                $formpre.append($("<input type='hidden' name='doing' value='online'/>")); 
                                $formpre.append($("<input type='hidden' name='RequestID' value="+reID+" />"));
                                $("body").append($formpre);
                                $formpre.submit(); 
                        }
                })
        })
        $(function(){
                $(".toback").click(function(){
                        if(window.confirm("真的要回滚吗？")){ //点击事件
                                var reID=$(this).attr("RequestID") //获取页面中的变量，这是ID
                                var CSRF403=$('[name="csrfmiddlewaretoken"]').val(); //获取name为csrf......的value
                                var User_ID=$('[name="user_id"]').val(); //获取name为user_id的value,操作者的id
                                var $formpre=$("<form action='/release/request/' method='post'></form>");
                                $formpre.append($("<input type='hidden' name='csrfmiddlewaretoken' value="+CSRF403+" />")); 
                                $formpre.append($("<input type='hidden' name='user_id' value="+User_ID+" />")); 
                                $formpre.append($("<input type='hidden' name='doing' value='toback'/>")); 
                                $formpre.append($("<input type='hidden' name='RequestID' value="+reID+" />"));
                                $("body").append($formpre);
                                $formpre.submit(); 
                        }
                })
        })
