/**
 * Created by tarena on 19-2-19.
 */
var user_reset_pwd_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        $(".form-group #save").click(function () {

            var btn_target = $(this);
            if (btn_target.hasClass("disabled")){
                common_ops.alert("正在处理!!请不要重复提交");
                return;
            }
            var old_password = $('.form-group input[id=old_password]').val();
            var new_password = $('.form-group input[id=new_password]').val();
            if(old_password==undefined || old_password.length < 1){
                common_ops.alert("请输入正确的密码");
                return
            }
            if(new_password==undefined || new_password.length < 1){
                common_ops.alert("请输入正确的密码");
                return
            }

            btn_target.addClass('disabled')

            $.ajax({
                url:common_ops.buildUrl('/user/reset-pwd'),
                type:'POST',
                data:{'old_password':old_password, 'new_password':new_password},
                dataType:'json',
                success:function (res) {
                    btn_target.removeClass("disabled");
                    if(res.code == 200){
                        callback = function(){
                            window.location.href = window.location.href;
                        }
                    }else{
                        callback = function () {

                        }
                    }
                    common_ops.alert(res.msg,callback)
                }
            })

        })
    }
};
$(document).ready(function () {
    user_reset_pwd_ops.init();
});
