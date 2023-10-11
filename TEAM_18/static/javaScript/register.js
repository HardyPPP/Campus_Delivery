function bindCaptchaButtonClick(){
    $("#captcha_btn").on("click", function (event){
        var $this = $(this); // get button
        var email = $("input[name = 'email']").val();// get email input
        if (!email){
            alert("please enter email");
            return;
        }
        $.ajax({
            url:"/user/captcha",
            method: "POST",
            data :{
                "email" :email
            },
            success: function (res){
                var code = res['code'];
                if (code === 200){
                    // lock the button, make it unclickable
                    $this.off("click");
                    // start timing
                    var countdown = 60;
                    var timer = setInterval(function (){
                        countdown = countdown - 1;
                        if(countdown > 0){
                            $this.text("Resend after " + countdown + " seconds");
                        }else{
                            $this.text("Get captcha");
                            // make the button clickable again
                            bindCaptchaButtonClick();
                            // reset the clock
                            clearInterval(timer);
                        }
                    }, 1000)
                    alert("sent successfully");
                }else{
                    alert(res['message']);
                }
            }
        });

    });
}


$(function(){
    bindCaptchaButtonClick();
});