$(document).ready(function(){
    $("#course_select").append("<option>7</option>");
    $("#course_select").change(function(){
        var checkText=$("#course_select").find("option:selected").text();
        //show table of courses
        console.debug(checkText);
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
    $('#dp').datepicker({format: 'yyyy-mm-dd', weekStart: 1}).on('changeDate', function(ev){
    date = formatdate(ev.date.getFullYear(), ev.date.getMonth() + 1, ev.date.getDate());
    console.debug(date);
    });
});
