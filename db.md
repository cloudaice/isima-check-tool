Student:

  * username: string
  * firstname: string
  * lastname: string
  * year： string like "2013"
  * group: string like (11, 12, 21, 22, 31, 32)
  * section: string like( F1, F2, F3, F4, F5, F6)
  * origin: string like FI or FC

Teacher:

  * username

Faculty:

  * username

Admin:

  * username

Course:

  * course_name： string
  * teacher_name: string
  * year: string 
  * sessions_num： int   the numbers of this course sessions
  * group: string
  * section: string
  * origin: string
  * students: list

Session:

  * course_name： string
  * teacher_name: string
  * date： date
  * interval_hour: string like "9:00-10:30"
  * filled：bool if this session is token
  * missing_students：list the usernames of all absence students

Justifying:

  * date: string session date
  * course_name: string
  * teacher_name: string
  * student_username: string 
  * kind_paper: the kind of absence like doctor
  * laptime: string the interval of absence time
  * reasom: the data of reason
