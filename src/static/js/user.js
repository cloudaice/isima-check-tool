$(document).ready(function(){
    var date = "";
    $("#course_select").hide();
    function show_select(courses){
        $("#course_select").empty();
        $("#course_select").append("<option>select course and teacher</option>");
        for(var i = 0; i < courses.length; i++){
            $("#course_select").append("<option>" + courses[i].course_name +
                                       " / " + courses[i].teacher_name + "</option>");
        }
        $("#course_select").show("slow");
        console.debug(courses);
    }

    function strip(str){
       if (str[0] == ' '){
           return strip(str.substring(1));
       }else if (str[str.length - 1] == ' '){
           return strip(str.substring(0, str.length - 1));
       }else{
           return str
       }
    }

    $("#course_select").change(function(){
        var checkText=$("#course_select").find("option:selected").text();
        if (checkText == "select course and teacher"){
            return;
        }
        var course_name = strip(checkText.split("/")[0]);
        var teacher_name = strip(checkText.split("/")[1]);
        var url = "/user/" + $.cookie("username")
        var param = {
            "request": "students",
            "date": date,
            "course_name": course_name,
            "teacher_name": teacher_name
        }
        $.ajax({
            type: 'POST',
            url: url,
            data: param,
            dataType: "json",
            success: function(data){
                console.debug(data); 
            }
        });
        console.debug(checkText);
        console.debug(course_name);
        console.debug(teacher_name);
    });
    
    function formatdate(year, month, day){
        if (month.toString().length == 1){
            month = '0' + month;
        }
        if (day.toString().length == 1){
            day = '0' + day;
        }
        return year + '-' + month + '-' + day;
    }

    $('#dp3').datepicker({format: 'yyyy-mm-dd', weekStart: 1}).on('changeDate', function(ev){
        date = formatdate(ev.date.getFullYear(), ev.date.getMonth() + 1, ev.date.getDate());
        var url = "/user/" + $.cookie("username")
        var param = {
            "request": "courses",
            "date": date
        }
        $.ajax({
            type: 'POST',
            url: url,
            data: param,
            dataType: "json",
            success: function(data){
                show_select(data);
            }
        });
    });
});
