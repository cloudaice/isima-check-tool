$(document).ready(function(){
    $("#loginform").ajaxForm(function(){
            $("#success").html("ok");
            window.location.href = "/";  
    });
});
