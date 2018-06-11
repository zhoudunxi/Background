//隐藏和显示SQL上线输入框
$(function () {
	$(".sql_hidden").css("display","none");//隐藏这个table标签
    $("#id_putsql").bind("change",function () { //当下拉菜单发生变化
	 	var sta_true = $('[name="putsql"]').val(); //获取当前下拉菜单选择的value
	 	if (sta_true=="none")
			$(".sql_hidden").css("display","none");//隐藏这个table标签
		else
			$(".sql_hidden").css("display","");//显示这个table标签 ,block 会修改css ，这里我用""
	})
})