
$(function () {
	 	var sta_true = $('[name="is_staff"]').val(); //获取当前下拉菜单选择的value
	 	if (sta_true=="True" || sta_true=="APKuser" || sta_true=="DBAuser")
			//$(".sel_hidden").attr("style","display:none;");//隐藏这个table标签
			$(".sel_hidden").css("display","none");//隐藏这个table标签
		else
		//	$(".sel_hidden").attr("style","display:block;");
			$(".sel_hidden").css("display","");//隐藏这个table标签 ,block 会修改css ，这里我用""
})


$(function () {
    $("#id_is_staff").bind("change",function () { //当下拉菜单发生变化
	 	var sta_true = $('[name="is_staff"]').val(); //获取当前下拉菜单选择的value
	 	if (sta_true=="True" || sta_true=="APKuser" || sta_true=="DBAuser")
			//$(".sel_hidden").attr("style","display:none;");//隐藏这个table标签
			$(".sel_hidden").css("display","none");//隐藏这个table标签
		else
		//	$(".sel_hidden").attr("style","display:block;");
			$(".sel_hidden").css("display","");//隐藏这个table标签 ,block 会修改css ，这里我用""

	})
})