from pymongo import Connection
from xlrd import open_workbook
import random

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
    index = random.randint(0, 5)
    return groups[index]


def CreateStudent():
    table = db.Student
    data = read_xls()
    docs = []
    for exame, lastname, firstname, student_username, section, teacher_username in data:
        docs.append({
            "username": student_username,
            "firstname": firstname,
            "lastname": lastname,
            "year": 2014,
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
    for exame, _, _, _, section, teacher_username in data:
        docs.append({
            "name": exame,
            "sessions_num": 24,
            "teacher": teacher_username,
            "section": section,
        })

    for doc in docs:
        condition = {
            "name": doc["name"],
            "teacher": doc["teacher"],
        }
        table.update(condition, doc, upsert=True)
        

def CreateSession():
    table = db.Session
    data = read_xls()
    docs = list()
    for exame, _, _, _, _, _, in data:
        docs.append({
            "course": exame,
            "date_hour": "2013-10-12-13:00",
            "filled": False,
            "missing_students": []
        })
    for doc in docs:
        condition = {
            "course": doc['course'],
        }
        table.update(condition, doc, upsert=True)


if __name__ == "__main__":
    #view_data()
    CreateSession()
    CreateTeacher()
    CreateAdmin()
    CreateCourse()
    CreateStudent()
