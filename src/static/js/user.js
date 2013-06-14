$(document).ready(function(){
    var date = "";
    var next_page = 0;

    //judge that which type of user
    if ($.cookie("type") == 'student'){
        $("#myTab li:eq(0)").remove();
        $("#myTab li:eq(0)").remove();
    }else if($.cookie("type") == "teacher"){
        $("#myTab li:eq(1)").remove();
    }else if($.cookie("type") == 'faculty'){
        $("#myTab li:eq(1)").remove();
    }else if($.cookie("type") != "admin"){
        $("#myTab li:eq(0)").remove();
        $("#myTab li:eq(0)").remove();
        $("#myTab li:eq(0)").remove();
    }

    function array2json(arr) {
        var parts = [];
        var is_list = (Object.prototype.toString.apply(arr) === '[object Array]');

        for(var key in arr) {
            var value = arr[key];
            if(typeof value == "object") { //Custom handling for arrays
                if(is_list) parts.push(array2json(value)); /* :RECURSION: */
                else parts[key] = array2json(value); /* :RECURSION: */
            } else {
                var str = "";
                if(!is_list) str = '"' + key + '":';
                if(typeof value == "number") str += value; //Numbers
                else if(value === false) str += 'false'; //The booleans
                else if(value === true) str += 'true';
                else str += '"' + value + '"'; //All other things
                parts.push(str);
            }
        }
        var json = parts.join(",");
        if(is_list) return '[' + json + ']';//Return numerical JSON
        return '{' + json + '}';//Return associative JSON
    }

    //load next absence page
    function load_absences(next_page){
        $.ajax({
            type: 'GET',
            url: "/reason",
            data: {"next_page": next_page},
            dataType: "json",
            success: function(data){
                if (data['status'] == "full"){
                    return
                }
                data = data['data'];
                var absence_table = "<hr><table class='table table-striped'>";
                absence_table += "<caption>Absences</caption>";
                absence_table += "<thead><tr><th>Date</th><th>Student Name</th><th>Course Name</th><th>kind_paper</th><th>laptime</th><th>reason</th></tr></thead>";
                absence_table += "<tbody>";
                for (var i = 0; i< data.length; i++){
                    absence_table += "<tr>"
                    absence_table += "<td>" + data[i]['date'] + "</td>";
                    absence_table += "<td>" + data[i]['student_username'] + "</td>";
                    absence_table += "<td>" + data[i]['course_name'] + "</td>";
                    absence_table += "<td>" + data[i]['kind'] + "</td>";
                    absence_table += "<td>" + data[i]['laptime'] + "</td>";
                    absence_table += "<td>" + data[i]['reason'] + "</td>";
                    absence_table += "</tr>";
                }
                absence_table += "</tbody></table>";
                $("#absence_table").html(absence_table);
            }
        });
    }

    // first load the absences list
    $('#myTab a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
        if ($(this).text() == "State"){
            load_absences(0);
            next_page = 10;
        }
    })

    //when click previous or next
    $("#paper a").click(function(e){
        e.preventDefault();
        var node_text = $(this).text();
        if (node_text == "Previous"){
            if (next_page > 10){
                next_page -= 20;
                load_absences(next_page);
                next_page += 10;
            }
        }else{
            load_absences(next_page);
            next_page += 10;
        }
    });

    function show_select(courses){
        $("#course_select").empty();
        $("#course_select").append("<option>select course and teacher</option>");
        for(var i = 0; i < courses.length; i++){
            $("#course_select").append("<option>" + courses[i].course_name +
                                       " / " + courses[i].teacher_name + "</option>");
        }
        $("#course_select").show("slow");
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
        var course_name = strip(checkText.substring(0, checkText.length - teacher_name.length - 2));
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
                student_table += "<thead><tr><th>Name</th><th>Absence</th><th>Reason</th></tr></thead>";
                student_table += "<tbody>";
                for(var i = 0; i < data.length; i++){
                    student_name = data[i];
                    student_table += "<tr><td><a data-name='/student' href='#' class='label label-success'>" + student_name + "</a></td>";
                    student_table += "<td><input data-checkbox='checkbox' type='checkbox'/></td>";
                    student_table += "<td><button data-edit='button' disabled='true' type='button' class='btn btn-small btn-primary disabled'>edit</button></td></tr>";
                }
                student_table += "</tbody></table>"
                student_table += "<div class='well'><button id='checksubmit'class='btn btn-large btn-block btn-primary' type='button'>Submit</button></div>";
                $("#stable").html(student_table);
                $("#checksubmit").click(function(){
                    var checked_data = new Array();
                    $("*[data-checkbox]").each(function(){
                        var e = $(this);
                        if(e.is(':checked')){
                            var date = $("#dp3 input").val();
                            var checkText=$("#course_select").find("option:selected").text();
                            var checktext_split = checkText.split("/");
                            var teacher_name = strip(checktext_split[checktext_split.length - 1]);
                            var course_name = strip(checkText.substring(0, checkText.length - teacher_name.length - 2));
                            var student_username = e.parent().prev("td").children().text();
                            checked_data.push({
                                "date": date,
                                "teacher": teacher_name,
                                "course": course_name,
                                "student": student_username
                            });
                        }
                    });
                    console.debug(array2json(checked_data));
                    $.ajax({
                        type: "POST",
                        url: "/session_absence",
                        data: {"absences": array2json(checked_data)},
                        dataType: "json",
                        success: function(data){
                            if (data["status"] == "success"){
                                $('#checkModalLabel').html('successed submit');
                                $('#checkModal').modal('show'); 
                            }else{
                                $('#checkModalLabel').html('some error with submit');
                                $('#checkModal').modal('show'); 
                            }
                        }
                    });
                });

                $("*[data-name]").hover( function(){
                    var e=$(this);
                    //$(this).unbind('mouseenter mouseleave');
                    var student_username = e.text();
                    $.ajax({
                        type: "GET",
                        url: "/student",
                        data: {"student_username": student_username},
                        dataType: "json",
                        success: function(data){
                            var info = "<span class='badge badge-info'>";
                            var content = "<p><i class='icon-user'></i>";
                            content += " " + data['lastname'] + "&nbsp;&nbsp;" + data['firstname'] + "</p>";
                            content += "<p>" + info + "Year: " + data['year'] + "</span>";
                            content += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
                            content += info + "Group: " + data['group'] + "</span></p>";
                            content += "<p>" + info + "Section: " + data['section'] + "</span>";
                            content += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
                            content += info + "Origin: " + data['origin'] + "</span></p>";
                            e.popover({
                                placement: 'top',
                                //title: student_username,
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

                $("*[data-name]").click(function(){
                    return false;
                });

                $("*[data-checkbox]").mousedown(function() {
                    if (!$(this).is(':checked')) {
                        //this.checked = confirm("Are you sure?");
                        //$(this).trigger("change");
                        $(this).parent().next("td").children().removeClass("disabled");
                        $(this).parent().next("td").children().removeAttr("disabled");
                    }else{
                        $(this).parent().next("td").children().addClass("disabled");
                        $(this).parent().next("td").children().attr("disabled", 'true');
                    }
                });

                $("*[data-edit]").click(function(){
                    $('#myModal').modal({
                        backdrop: true,
                        keyboard: true,
                        show: true
                    });
                    e = $(this);
                    $("#reasonsubmit").click(function(){
                        var date = $("#dp3 input").val();
                        var checkText=$("#course_select").find("option:selected").text();
                        checktext_split = checkText.split("/");
                        var teacher_name = strip(checktext_split[checktext_split.length - 1]);
                        var course_name = strip(checkText.substring(0, checkText.length - teacher_name.length - 2));
                        var student_username = e.parent().prev("td").prev("td").children().text();
                        var kind = $("#inputKind").val();
                        var laptime = $("#inputLaptime").val();
                        var reason = $("#inputReason").val();
                        var param = {
                            "student_username": student_username,
                            "kind": kind,
                            "laptime": laptime,
                            "reason": reason,
                            "course_name": course_name,
                            "teacher_name": teacher_name,
                            "date": date
                        }
                        $.ajax({
                            type: 'POST',
                            url: '/reason',
                            data: param,
                            dataType: "json",
                            success: function(data){
                                if (data.status == "success"){
                                    $('#myModal').modal('hide');
                                }else{
                                    //alert(data.msg);
                                    jAlert('Alert box', data.msg);
                                }
                            }
                        });
                        return false;
                    });
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

    $("#dp3").popover({
        placement: 'bottom',
        trigger: "hover",
        content: "Please select date",
        delay: 0
    });

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
