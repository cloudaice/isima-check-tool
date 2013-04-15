$(document).ready(function(){
    function validate(formData, jqForm, options){
        for(var i=0; i < formData.length; i++){
            if(!formData[i].value){
                $("#alert_result").addClass("alert alert-error");
                $("#alert_result").html(formData[i].name + " can not be empty!");
                return false
            }
        }
        var querystring = $.param(formData)
        return true
    }
    function success_do(data){
        if (data.status == "error"){
            $("#alert_result").addClass("alert alert-error");
            $("#alert_result").html(data.msg);
        }else{
            location.href = "/"
        }
    }
    var options = {
        target:"#alert_result",
        beforeSubmit: validate,
        success: success_do,
        dataType: "json",
        resetForm: true
    }
    $("#loginform").submit(function(){
        $(this).ajaxSubmit(options);
        return false;
    });
});
