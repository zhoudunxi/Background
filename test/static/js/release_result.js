//上线列表失败状态详情查看入口
$(function () {
    var obj = $(".release_status");
    var pattern = /失败/;
    obj.each(function() {
        var status = $(this).html();
        if (pattern.test(status)) {
            $(this).siblings().css("display", "inline");
            $(this).siblings().css("cursor", "pointer");
            $(this).siblings().attr("title", "点我查看详细信息");
        }
    })
})
//获取上线失败结果详情
function _get_release_result(release_id) {
    var csrf = $("[name='csrfmiddlewaretoken']").val();
    $.post("/release/uploadstatus/",
    {"csrfmiddlewaretoken":csrf,
    "release_id":release_id},
    function(output) {
        var data = JSON.parse(output);
        if (data.establisherror.length > 0) {
            var establisherror_head = "以下服务器连接失败:\n"
            var establisherror_body = '';
            for (var i=0; i<data.establisherror.length; i++) {
                establisherror_body = establisherror_body+data.establisherror[i]+"\n"
            }
            var establisherror = establisherror_head + establisherror_body;
        }
        else {
            var establisherror = '';
        }

        if (data.nonexistent.length > 0) {
            var nonexistent_head = "以下文件不存在:\n"
            var nonexistent_body = '';
            for (var l=0; l<data.nonexistent.length; l++) {
                nonexistent_body = nonexistent_body+data.nonexistent[l]+"\n"
            }
            var nonexistent = nonexistent_head + nonexistent_body;
        }
        else {
            var nonexistent = '';
        }

        if (data.syntaxerror.length > 0) {
            var syntaxerror_head = "以下PHP脚本存在语法错误:\n"
            var syntaxerror_body = '';
            for (var m=0; m<data.syntaxerror.length; m++) {
                syntaxerror_body = syntaxerror_body+data.syntaxerror[m]+"\n"
            }
            var syntaxerror = syntaxerror_head + syntaxerror_body;
        }
        else {
            var syntaxerror = '';
        }

        var all_uploaderror = data.uploaderror;
        var uploaderror_head = "以下文件发布失败:\n";
        var uploaderror_body = '';
        for (var k in all_uploaderror) {
            var fail_files = k + ':\n' + all_uploaderror[k].join('\n') + '\n';
            uploaderror_body = uploaderror_body + fail_files;
        }
        if (uploaderror_body.length > 0) {
            var uploaderror = uploaderror_head + uploaderror_body;
        }
        else {
            var uploaderror = '';
        }

        var release_error = establisherror + nonexistent + syntaxerror + uploaderror;
        if (release_error.length > 0) {
            alert(release_error);
        }
        else {
            return 'success';
        }
    })
}

function get_release_result(obj) {
    var release_id = $(obj).parents('td').siblings('#release_id').html();
    _get_release_result(release_id);
}

$(function () {
    var status_pattern = /fail/;
    var id_pattern = /requestid/;
    var url = location.search;
    if (url.indexOf('?') != -1) {
        var urls = url.split('&');
        for (var u=0; u<urls.length; u++) {
            if (id_pattern.test(urls[u])) {
                var release_id = urls[u].split('=')[1];
            }
            if (status_pattern.test(urls[u])) {
                var release_status = true;
            }
        }
    }
    else {
        return;
    }
    if (release_status) {
        _get_release_result(release_id);
    }
})