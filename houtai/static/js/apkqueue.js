var CSRF403=$('[name="csrfmiddlewaretoken"]').val(); //获取name为csrf......的value
var IDLIST=$('[name="queue_idstr"]').val(); //获取队列id字符串

var int=self.setInterval("editpercent()",2000)
function editpercent(){
        $.post("/apkupdate/apkqueue/qstatus",
                {"csrfmiddlewaretoken":CSRF403,"queue_idstr":IDLIST},
                function(outdata) {
                //      console.log(outdata) //调试，打印outdata
                        var data = JSON.parse(outdata);
                        //console.log(data)     
                        for (var key in data){
                            var id = key
                            var per = data[key].percent
                            var done = data[key].done_message
                            var total = data[key].total_message
                            //console.log(id + ',' + per + ',' + done + ',' + total)
                            $('#DStatusID' + id).html(done + '/' + total)
                            $('#DStatusID' + id).parent().css('width', per + '%')
                            $('#DStatusID' + id).parent().attr('aria-valuenow', per)
                        }
                }
        );
}
