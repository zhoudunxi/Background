function peizhi() {
         $(".homeactive2,.active").each(function(){
             var Menu = $(this).find("a").text()
                if (Menu === "配置管理"){
                        $(this).empty()
                        $(this).addClass("dropdown")
                        $(this).append('<a href="#" class="dropdown-toggle homea" data-toggle="dropdown">'+
                                        '配置管理'+
                                        '<b class="caret"></b>'+
                                        '</a>'+
                                        '<ul class="dropdown-menu">'+
                                        '<li><a href="/configures/php/">Php配置文件</a></li>'+
                                        '<li class="divider"></li>'+
                                        '<li><a href="#">Nginx配置文件</a></li>'+
                                        '</ul>')
                }
         })
}