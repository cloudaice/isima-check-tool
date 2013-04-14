Student:
  * username
  * first_name
  * last_name
  * year： 学生毕业年份
  * group(11, 12, 21, 22, 31, 32)
  * section( F1, F2, F3, F4, F5, F6)
  * origin FI or FC

Teacher:
  * username

Faculty:
  * username

Admin:
  * username

Course:
  * name：课程名字
  * sessions_num： 多少节课
  * teacher：授课老师
    - year
    - group
    - section
    - origin

Session:
  * course：课程名字
  * date_hour：上课时间
  * filled：是否有学生没有来
  * missing_students：请假学生的列表

Justifying:
  * student_name: lastname_firstname
  * laptime: 请假的区间
  * kind_paper: 假的类别

