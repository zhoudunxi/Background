                var addstatus=$('[name="addstatus"]').val();
                if(addstatus=="success") {
                    alert("添加项目成功！");
                }
                var editstatus=$('[name="editstatus"]').val();
                if(editstatus=="success") {
                    alert("更新项目成功！");
                    history.go(-2);
                }
                else if (editstatus=="invalid") {
                    alert("提交的数据不合法,更新失败！");
                    history.go(-1);
                }