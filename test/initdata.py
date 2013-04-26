from pymongo import Connection
from xlrd import open_workbook
import random
import datetime

cnn = Connection("localhost", 27017)
db = cnn["isima"]


def read_xls():
    filename = "../../graph-color/docs/zz3.xls"
    wb = open_workbook(filename)
    docs = list()
    for s in wb.sheets():
        for row in range(2, s.nrows):
            values = []
            for col in range(s.ncols):
                values.append(s.cell(row, col).value)
            exame = '-'.join(values[0].strip().split())
            lastname = values[1].strip()
            firstname = values[2].strip()
            student_username = lastname + firstname
            section = values[3].strip()
            teacher_username = ''.join(values[4].strip().split(' '))
            docs.append((exame, lastname, firstname, student_username,
                         section, teacher_username))
        break
    return docs


def get_date(year, month, day):
    day = datetime.datetime(year, month, day)
    while True:
        interval = random.randint(1, 4)
        next_day = day + datetime.timedelta(days=interval)
        day = next_day
        yield next_day.strftime("%Y-%m-%d")


def view_data():
    docs = read_xls()
    for exame, lastname, firstname, student_username, section, teacher_username in docs:
        print "exame:", exame
        print "lastname:", lastname
        print "firstname:", firstname
        print "student_username:", student_username
        print "section:", section
        print "teacher_username:", teacher_username


def random_group():
    groups = ['11', '12', '21', '22', '31', '32']
    return random.choice(groups)


def random_year():
    years = ["2012", "2013", "2014", "2015"]
    return random.choice(years)


def random_hour():
    hours = ["08:00-10:00", "10:00-12:00", "08:00-09:30", "13:00-15:00", "15:00-17:00", "13:30-15:30"]
    return random.choice(hours)


def CreateStudent():
    table = db.Student
    data = read_xls()
    docs = []
    for exame, lastname, firstname, student_username, section, teacher_username in data:
        docs.append({
            "username": student_username,
            "firstname": firstname,
            "lastname": lastname,
            "year": random_year(),
            "group": random_group(),
            "section": section,
            "origin": "FI"
        })
    for doc in docs:
        condition = {
            "username": doc["username"]
        }
        table.update(condition, doc, upsert=True)


def CreateTeacher():
    table = db.Teacher
    data = read_xls()
    for _, _, _, _, _, teacher in data:
        doc = {
            "username": teacher
        }
        condition = doc
        table.update(condition, doc, upsert=True)


def CreateAdmin():
    table = db.Admin
    table.update({"username": "admin"}, {"username": "admin"}, upsert=True)


def CreateCourse():
    table = db.Course
    data = read_xls()
    docs = list()
    for exame, _, _, student_username, section, teacher_username in data:
        docs.append({
            "course_name": exame,
            "teacher_name": teacher_username,
            "year": "2013",
            "section": section,
            "group": random_group(),
            "origin": "FI",
            "sessions_num": 24,
            "students": [student_username
                    for this_exame, _, _, student_username, section, this_teacher_username in data
                    if exame == this_exame and teacher_username == this_teacher_username
                         ]
        })

    for doc in docs:
        condition = {
            "course_name": doc["course_name"],
            "teacher_name": doc["teacher_name"],
            "year": doc["year"]
        }
        table.update(condition, doc, upsert=True)


def CreateSession():
    table = db.Session
    docs = list()
    cursor = db.Course.find({}, {"course_name": 1, "teacher_name": 1, "year": 1})
    for doc in cursor:
        date = get_date(int(doc["year"]), 03, 23)
        for _ in range(24):
            docs.append({
                "course_name": doc["course_name"],
                "teacher_name": doc["teacher_name"],
                "date": date.next(),
                "interval_hour": random_hour(),
                "filled": False,
                "missing_students": []
            })
    for doc in docs:
        condition = {
            "course_name": doc["course_name"],
            "teacher_name": doc["teacher_name"],
            "date": doc["date"]
        }
        table.update(condition, doc, upsert=True)


if __name__ == "__main__":
    #view_data()
    CreateStudent()
    CreateTeacher()
    CreateAdmin()
    CreateCourse()
    CreateSession()
