#-*-coding: utf-8-*-
# @author: xiangchao<cloudaice@gmail.com>

import json
import os
from lib import Mongo
from tornado import gen
from tornado import web
from tornado import ioloop
from tornado.httpserver import HTTPServer
from tornado.options import define, parse_command_line, options
from tornado.escape import json_encode


define("host", default="127.0.0.1", help="run on the given host")
define("port", default=8000, help="run on the given port", type=int)
define("mongo_host", default="localhost", help="isima mongo host")
define("mongo_port", default=27017, help="run on default port", type=int)


class Application(web.Application):
    def __init__(self):
        settings = {
            "static_path": os.path.join(os.path.dirname(__file__), 'static'),
            "template_path": os.path.join(os.path.dirname(__file__), 'template'),
            "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            "login_url": "/login",
            "xsrf_cookies": False,
            "debug": True
        }

        handlers = [
            (r"/", Home),
            (r"/about", About),
            (r"/contact", Contact),
            (r"/user/([^/]+)", User),
            (r"/student", Student),
            (r"/reason", Reason),
            (r"/session_absence", Session_absence),
            (r"/login", Login),
            (r"/logout", Logout),
            (r"/favicon.ico", web.StaticFileHandler, dict(path=settings['static_path'])),
        ]

        web.Application.__init__(self, handlers, **settings)

        self.db = Mongo.conn(options.mongo_host, options.mongo_port)['isima']


class BaseHandler(web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    
    def get_current_user(self):
        user_id = self.get_secure_cookie("isima_user")
        if not user_id:
            return None
        # this may instead of real user
        return user_id


class Home(BaseHandler):
    def get(self):
        self.render('home.html')


class About(BaseHandler):
    def get(self):
        self.render('about.html')


class Contact(BaseHandler):
    def get(self):
        self.render('home.html')


class Login(BaseHandler):
    def get(self):
        if not self.get_cookie("checking"):
            self.set_cookie('checking', 'true')
        self.render('login2.html')

    def auth_password(self, password):
        """
        do something auth the password
        """
        pass
    
    @web.asynchronous
    @gen.coroutine
    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        rememberme = self.get_argument("rememberme", None)
        resp = yield gen.Task(self.verify_user, username, password)
        if resp["status"] == "success":
            if not rememberme:
                self.set_secure_cookie("isima_user", username, expires_days=1)
            else:
                self.set_secure_cookie("isima_user", username)
        self.write(json_encode(resp))
        self.finish()

    def verify_user(self, username, password, callback=None):
        docs = self.db.Student.find({}, {"username": 1})
        docs = [doc["username"] for doc in docs]
        if username in docs:
            self.auth_password(password)
            callback({
                "status": "success",
                "direct": "/user/" + username,
                "type": "student"
            })
        docs = self.db.Teacher.find({}, {"username": 1})
        docs = [doc["username"] for doc in docs]
        if username in docs:
            self.auth_password(password)
            callback({
                "status": "success",
                "direct": "/user/" + username,
                "type": "teacher"
            })
        docs = self.db.Faculty.find({}, {"username": 1})
        docs = [doc["username"] for doc in docs]
        if username in docs:
            self.auth_password(password)
            callback({
                "status": "success",
                "direct": "/user/" + username,
                "type": "faculty"
            })
        docs = self.db.Admin.find({}, {"username": 1})
        docs = [doc["username"] for doc in docs]
        if username in docs:
            self.auth_password(password)
            callback({
                "status": "success",
                "direct": "/user/" + username,
                "type": "admin"
            })


class Logout(BaseHandler):
    @web.authenticated
    def get(self):
        self.clear_cookie("isima_user")
        self.redirect("/")


class User(BaseHandler):
    @web.authenticated
    def get(self, username):
        self.render("user.html")
    
    @web.authenticated
    @web.asynchronous
    @gen.coroutine
    def post(self, username):
        request = self.get_argument("request")
        date = self.get_argument("date")
        resp = None
        if request == "courses":
            resp = yield gen.Task(self.get_courses, date)
        elif request == "students":
            course_name = self.get_argument("course_name")
            teacher_name = self.get_argument("teacher_name")
            resp = yield gen.Task(self.get_students, date, course_name, teacher_name)
        self.write(json_encode(resp))
        self.finish()

    def get_courses(self, date, callback=None):
        cursor = self.db.Session.find({"date": date},
                                      {"course_name": 1,
                                       "teacher_name": 1,
                                       "interval_hour": 1
                                       })
        docs = list()
        for doc in cursor:
            del doc["_id"]
            docs.append(doc)
        callback(docs)

    def get_students(self, date, course_name, teacher_name, callback=None):
        year = date.split("-")[0]
        cursor = self.db.Course.find({"course_name": course_name,
                                      "teacher_name": teacher_name,
                                      "year": year
                                      }, {"students": 1})
        docs = list()
        for doc in cursor:
            del doc["_id"]
            docs.extend(doc["students"])
        callback(docs)


class Student(BaseHandler):
    @web.authenticated
    @web.asynchronous
    @gen.coroutine
    def get(self):
        student_username = self.get_argument("student_username", None)
        resp = yield gen.Task(self.get_students, student_username)
        self.write(json_encode(resp))
        self.finish()
        
    def get_students(self, student_username, callback=None):
        cursor = self.db.Student.find({"username": student_username})
        docs = list()
        for doc in cursor:
            del doc["_id"]
            docs = doc
        callback(docs)
            

class Reason(BaseHandler):
    @web.authenticated
    @web.asynchronous
    @gen.coroutine
    def get(self):
        next_page = self.get_argument("next_page")
        next_page = int(next_page)
        resp = yield gen.Task(self.get_reasons, next_page)
        self.write(json_encode(resp))
        self.finish()

    def get_reasons(self, next_page, callback=None):
        all_reasons = self.db.Justifying.find().count()
        if all_reasons < next_page:
            callback({"status": "full"})
        cursor = self.db.Justifying.find({}, sort=[{"date", -1}]).skip(next_page).limit(10)
        docs = list()
        for doc in cursor:
            del doc["_id"]
            del doc["teacher_name"]
            docs.append(doc)
        callback({"status": "ok", "data": docs})

    def post(self):
        course_name = self.get_argument("course_name")
        teacher_name = self.get_argument("teacher_name")
        date = self.get_argument("date")
        kind = self.get_argument("kind")
        laptime = self.get_argument("laptime")
        reason = self.get_argument("reason")
        student_username = self.get_argument("student_username")
        condition = {
            "date": date,
            "course_name": course_name,
            "teacher_name": teacher_name,
        }
        docs = {
            "date": date,
            "course_name": course_name,
            "teacher_name": teacher_name,
            "student_username": student_username,
            "kind": kind,
            "laptime": laptime,
            "reason": reason
        }
        self.db.Justifying.update(condition, docs, upsert=True)
        self.write(json_encode({"status": "success"}))
        self.finish()
    

class Session_absence(BaseHandler):
    @web.authenticated
    def post(self):
        absences = self.get_argument("absences", None)
        if not absences:
            print "no absence"
            self.write(json_encode({"status": "failed"}))
            self.finish()
            return
        absences = json.loads(absences)
        print type(absences)
        for check in absences:
            date = check["date"]
            teacher_name = check["teacher"]
            course_name = check["course"]
            student_username = check["student"]
            doc = self.db.Session.find_one({"teacher_name": teacher_name,
                                            "date": date,
                                            "course_name": course_name})
            if not doc:
                print 'no doc'
                self.write(json_encode({"status": "failed"}))
                self.finish()
                return
            if student_username not in doc["missing_students"]:
                doc["missing_students"].append(student_username)
            doc["filled"] = True
            self.db.Session.update({"teacher_name": teacher_name,
                                    "date": date,
                                    "course_name": course_name}, doc)
        self.write(json_encode({"status": "success"}))
        self.finish()


def main():
    parse_command_line()
    http_server = HTTPServer(Application())
    http_server.listen(options.port, options.host)
    ioloop.IOLoop.instance().start()
    

if __name__ == "__main__":
    main()
