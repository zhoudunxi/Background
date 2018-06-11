var flng = true
$(function(){
	$(".buildapk").click(function(){
		if (flng){
		flng = false;
		//$('#buildapkid').attr("true","disabled");
		var CSRF403=$('[name="csrfmiddlewaretoken"]').val(); //获取name为csrf......的value
		var User_ID=$('[name="user_id"]').val(); //获取name为user_id的value,操作者的id
		var Project = $('[name="project"]').find('option:selected').val();
		var Version = $('#id_apkversion_' + Project).find('option:selected').val();
		var Priority = $('[name="queue_priority"]').val();
      		//var Version = $('[name="apkversion"]').val();
      		var Identify = $('[name="identify"]').val();
		//if (Identify.split("\n").length > 20) {
		//	alert("一次最多只能处理20条，请重新输入。");
		//	return
		//};
		//console.log(Project)
		
		if (Version==''){
			$('#PversionEid').html("版本号：不能为空！");
                        $("#versionEid").removeClass("hidden").addClass("show");
			flng = true
			}
		if (Identify==''){
			$('#PidentifyEid').html("渠道标识：不能为空！");
                        $("#identifyEid").removeClass("hidden").addClass("show");
			flng = true
			}
		if (Version!=='' && Identify!==''){
			$.post("/apkupdate/apkrequest/",
			{"csrfmiddlewaretoken":CSRF403,
			"project_name":Project,
			"user_id":User_ID,
			"queue_priority":Priority,
			"apkversion":Version,
			"identify":Identify},
			function(output) {
				var data = JSON.parse(output);
				if (data.result ==  1) {
					alert("提交失败！输入的版本号不存在！");
				}
				else if (data.result == 2) {
					alert("----下次报错写这里-----");
				}
				else if (data.result == 0) {
					alert("您提交的事务正在处理，耗时可能较长，请到‘APK队列’中查看状态！");
				}
				window.location.href=window.location.href;
			});
		}
}
      })
})
