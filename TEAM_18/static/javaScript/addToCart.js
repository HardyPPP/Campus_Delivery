function bindAddButtonClick(){
    $(".add_to_cart").on("click", function (event){
        var $this = $(this); // get button
        var commodity = $(".commodity_idQ").val();// get email input
        if (commodity){
            alert(commodity);
        }else{
             alert("nocommodity");
        }
        //using ajax to call the add func in the backend
        $.ajax({
            url:"/order/addNewOrder",
            method: "POST",
            //deliver the commodity data
            data :{
                "commodity_id" :commodity
            },
            success: function (res){
                alert($this.innerText);
                var code = res['code'];
                if (code === 200){
                    alert("add successfully");
                }else{
                    alert(res['message']);
                }
            }
        });

    });
}


$(function(){
    bindAddButtonClick();
});