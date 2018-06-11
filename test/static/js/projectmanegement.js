        $(function(){
                $(".DeleteSto").click(function(){
                        var StoID = $(this).attr("sto-id");//获取html中的变量
                        var StoName=$(this).attr("sto-name");//获取html中的变量
                        if(window.confirm("警告！是否确认仓库 "+StoName+" ?")){ //点击事件
                                window.location.href="/projectmanegement/?deletestorage="+StoID; //用同步的方式get到后端服务器
                        }
                })
                $(".DeletePro").click(function(){
                        var ProID = $(this).attr("pro-id");//获取html中的变量
                        var ProName=$(this).attr("pro-name");//获取html中的变量
                        if(window.confirm("警告！是否要删除项目 "+ProName+" ?")){ //点击事件
                                window.location.href="/projectmanegement/?deleteproject="+ProID; //用同步的方式get到后端服务器
                        }
                })
     	})
