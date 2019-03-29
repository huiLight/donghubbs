function notify(id){
    content = "该字段不能为空"
    if(arguments.length==2){
        content = arguments[1];
    }
    $(id).text(content)

    setTimeout(function(){$(id).text("")}, 3000)
}

// 验证用户名是否可用
$("#username").blur(function(){
    if ($("#username").val() != ""){
        $.ajax({
            url: "/sendcode/code",
            headers:{"X-CSRFToken":$.cookie('csrftoken')},
            data: {species:2, username: $("#username").val()},
            dataType: "json",
            type: "post",
            async: false,
            chache: false,
            success: function(name){
                if(name['namestate']){
                    $("#namewrong").text("√");
                }else{
                    $("#namewrong").text("用户名已存在");
                }
            },
        });
    }
});

// 提交表单
$("#submit").click(function(){
    
    if($("#username").val()==""){
        notify('#namewrong');
        return;
    }
    if($("#useremail").val()==""){
        notify('#emailwrong');
        return;
    }
    if($("#yzm").val()==""){
        notify('#yzmwrong');
        return;
    }
    if(pwdIsWrong()){
        return;
    }
    if($("#repassword").val()==""){
        notify('#rpwdwrong');
        return;
    }else if($("#password").val() != $("#repassword").val()){
        $("#rpwdwrong").text("两次密码不一致");
        return;
    }

    $.ajax({
        url: "/register/",
        headers:{"X-CSRFToken":$.cookie('csrftoken')},
        data: {username:$("#username").val(),
                email: $("#useremail").val()+'@lcu.edu.cn',
                yzm: $("#yzm").val(),
                password: $("#password").val()},
        dataType: "json",
        type: "post",
        async: false,
        chache: false,
        success: function(info){
            if(info['success']){
                window.location.href='/'
            }else{ // 注册失败
                // 用户名已存在
                if(info['state'] & 1){
                    notify("#namewrong", "用户名已存在")
                }
                // 邮箱已注册
                if(info['state'] & 2){
                    notify("#emailwrong", "邮箱已注册")
                }
                // 验证码错误
                if(info['state'] & 4){
                    notify("#yzmwrong", "验证码错误");
                }
            }
        },
    });

});

$("#repassword").keyup(function(){
    if ($("#password").val() == $("#repassword").val()) {
        $("#rpwdwrong").text("")
    }
});

// 验证验证码是否正确
$("#yzm").blur(function(){
    if ($("#yzm").val() != ""){
        $.ajax({
            url: "/sendcode/code",
            headers:{"X-CSRFToken":$.cookie('csrftoken')},
            data: {species:1, yzm: $("#yzm").val()},
            dataType: "json",
            type: "post",
            async: false,
            chache: false,
            success: function(yzm){
                if(yzm['state']){
                    $("#yzmwrong").text("");
                }else{
                    $("#yzmwrong").text("验证码错误");
                }
            },
        });
    }
});


// $("#password").blur(pwdIsWrong());

// 密码长度大于8
function pwdIsWrong(){
    if($("#password").val().length<8){
        $("#pwdwrong").text("密码长度需大于8位");
        return true;
    }else{
        $("#pwdwrong").text("");
    }
    // TODO: 验证密码包含字母、数字和符号
    return false;
}


$("#second").click(function (){
    sendyzm($("#second"));
});
//用ajax提交到后台的发送邮箱接口
function sendyzm(obj){            
    var email = $("#useremail").val();
    var result = isEmail();
    if(result) {
        $.ajax({
            url:"/sendcode/",
            headers:{"X-CSRFToken":$.cookie('csrftoken')},
            data:{email: email},
            dataType:"json",
            type:"post",
            async : false,
            cache : false,
            success:function(res){
                // debugger;
                if(res){
                    alert("验证码发送成功");
                }else{

                }
            },
            error:function(){
                alert("验证码发送失败");
            }
        })
        setTime(obj);//开始倒计时
    }
}

//60s倒计时实现逻辑
var countdown = 60;
function setTime(obj) {
    if (countdown == 0) {
        obj.prop('disabled', false);
        obj.text("点击获取验证码");
        countdown = 60;//60秒过后button上的文字初始化,计时器初始化;
        return;
    } else {
        obj.prop('disabled', true);
        obj.text("("+countdown+"s)后重新发送") ;
        countdown--;
    }
    setTimeout(function() { setTime(obj) },1000) //每1000毫秒执行一次
}


//校验号是否合法
function isEmail(){
    var phonenum = $("#useremail").val();
    var reg = /^(\d{10})$/;
    if(!reg.test(phonenum)){
        alert('请输入有效的邮箱号码！');
        return false;
    }else{
        return true;
    }
}