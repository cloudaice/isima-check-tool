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
        checktext_split = checkText.split("/");
        var teacher_name = strip(checktext_split[checktext_split.length - 1]);
        var course_name = checkText.substring(0, checkText.length - teacher_name.length - 2);
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
                var student_table = "<hr><table class='table table-striped'>";
                student_table += "<caption>Students</caption>";
                student_table += "<thead><tr><th>Name</th><th>Fill</th><th>Reason</th></tr></thead>";
                student_table += "<tbody>";
                for(var i = 0; i < data.length; i++){
                    student_name = data[i];
                    student_table += "<tr><td><a data-name='/student' href='#' class='label label-success'>" + student_name + "</a></td>";
                    student_table += "<td><input data-checkbox='checkbox' type='checkbox'/></td>";
                    student_table += "<td><button disabled='true' type='button' data-toggle='modal' data-target='#myModal' class='btn btn-small btn-primary disabled'>add</button></td></tr>";
                }
                student_table += "</tbody></table>"
                $("#stable").html(student_table);
                $("*[data-name]").hover( function(){
                    console.debug("in");
                    var e=$(this);
                    console.debug(e.text());
                    //$(this).unbind('mouseenter mouseleave');
                    var student_username = e.text();
                    $.ajax({
                         type: "GET",
                         url: "/student",
                         data: {"student_username": student_username},
                         dataType: "json",
                         success: function(data){
                             var content = ""
                             for (k in data){
                             content += " " + k + ":" + data[k];
                             }
                             e.popover({
                                  placement: 'top',
                                  title: student_username,
                                  content: content,
                                  html: true,
                                  triggrt: "hover",
                                  delay: 0
                             }
                             ).popover("show");
                         }
                    });
                }, function(){
                    var e = $(this);
                    e.popover("hide");
                });
                $("*[data-poload]").bind("click", function(){
                    return false;
                });

                $("*[data-checkbox]").mousedown(function() {
                    if (!$(this).is(':checked')) {
                        //this.checked = confirm("Are you sure?");
                        //$(this).trigger("change");
                        console.debug("check");
                        $(this).parent().next("td").children().removeClass("disabled");
                        $(this).parent().next("td").children().removeAttr("disabled");
                    }else{
                        $(this).parent().next("td").children().addClass("disabled");
                        $(this).parent().next("td").children().attr("disabled", 'true');
                        console.debug("uncheck");
                    }
                });
            }
        });
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
