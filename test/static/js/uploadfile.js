function upload(Projectid,obj,env) {
	//chrome IE10
	var csrf = $("[name='csrfmiddlewaretoken']").val();
	var projectid = Projectid ;
	console.log(env)
	if (window.FileReader) {
		var file = obj.files[0];
		console.log(file)
		var re=/(.[.]conf)$|(.[.]config)$|(.[.]php)$|(.[.]html)$/i;
		if (!re.test(file.name)) {
			alert('请选择正确的文件文件类型！');
			window.location.href = window.location.href;
			return;
		}
		var reader = new FileReader();
		reader.readAsText(file);
		reader.onload = function() {
			$.post("/configures/api/phpfpm/upload/",
    		{"csrfmiddlewaretoken":csrf,
			"projectid":projectid,
			"filename":file.name,
			"env":env,
			"content":this.result},
    		function(output) {
				var data = JSON.parse(output);
				if (data.status == 'success') {
					//alert('文件上传成功');
					layer.alert("文件上传成功",function(){
                    window.location.reload();
                });
				}
				else {
					layer.alert("文件上传失败:<br>"+data.data,function(){
                    window.location.reload();
                });
				}
			})		
		}
	} 
	//IE 7 8 9 10
	/*
	else if (typeof window.ActiveXObject != 'undefined'){
		var xmlDoc; 
		xmlDoc = new ActiveXObject("Microsoft.XMLDOM"); 
		xmlDoc.async = false; 
		xmlDoc.load(obj.value); 
		alert(xmlDoc.xml); 
	} 
	//FF
	else if (document.implementation && document.implementation.createDocument) { 
		var xmlDoc; 
		xmlDoc = document.implementation.createDocument("", "", null); 
		xmlDoc.async = false; 
		xmlDoc.load(obj.value); 
		alert(xmlDoc.xml);
	} else { 
		alert('error'); 
	}
	*/
}