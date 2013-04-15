$(document).ready(function(){
    url = window.location.href;
    lasturl = url.split('/');
    classname = '/' + lasturl[lasturl.length-1]; 
    idname = '#' + lasturl[lasturl.length-1]
    if (classname == '/'){
        $('#home').addClass('active');
    }else{
    $(idname).addClass('active');
    }    
    if ($.cookie("isima_user")){
        var username = $.cookie("username")
        $("#login").html("<a href='/logout'>Logout</a>");
        $("#home").html("<a href='/user/" + username +"'>Home</a>")
    }else{
        $("#login").html("<a href='/login'>Login</a>");
    }
});
