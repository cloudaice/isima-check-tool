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
});