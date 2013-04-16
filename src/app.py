#-*-coding: utf-8-*-
# @author: xiangchao<cloudaice@gmail.com>

import os
from lib import Mongo
#from tornado import gen
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

    def post(self):
        #判断浏览器是否启用了cookie
        if not self.get_cookie("checking"):
            self.write("please enable cookies!")
            self.finish()
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        rememberme = self.get_argument("rememberme", None)
        docs = self.db.Student.find({}, {"username": 1})
        docs = [doc["username"] for doc in docs]
        if username in docs:
            self.auth_password(password)
            if not rememberme:
                self.set_secure_cookie("isima_user", username, expires_days=1)
            else:
                self.set_secure_cookie("isima_user", username)
            self.write(json_encode({
                "status": "success",
                "direct": "/user/" + username,
                "type": "student"
            }))
            self.finish()
            return
        docs = self.db.Teacher.find({}, {"username": 1})
        docs = [doc["username"] for doc in docs]
        if username in docs:
            self.auth_password(password)
            if not rememberme:
                self.set_secure_coolie("isima_user", username, expires_days=1)
            else:
                self.set_secure_cookie("isima_user", username)
            self.write(json_encode({
                "status": "success",
                "direct": "/user/" + username,
                "type": "teacher"
            }))
            self.finish()
            return
        docs = self.db.Faculty.find({}, {"username": 1})
        docs = [doc["username"] for doc in docs]
        if username in docs:
            self.auth_password(password)
            if not rememberme:
                self.set_secure_cookie("isima_user", username, expires_days=1)
            else:
                self.set_secure_cookie("isima_user", username)
            self.write(json_encode({
                "status": "success",
                "direct": "/user/" + username,
                "type": "faculty"
            }))
            self.finish()
            return
        docs = self.db.Admin.find({}, {"username": 1})
        docs = [doc["username"] for doc in docs]
        if username in docs:
            self.auth_password(password)
            if not rememberme:
                self.set_secure_cookie("isima_user", username, expires_days=1)
            else:
                self.set_secure_cookie("isima_user", username)
            self.write(json_encode({
                "status": "success",
                "direct": "/user/" + username,
                "type": "admin"
            }))
            self.finish()
            return
        self.write(json_encode({"status": 'error', "msg": "no this user"}))
        self.finish()


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
    def post(self, username):
        request = self.get_argument("request")
        if request == "courses":
            date = self.get_argument("date")
            cursor = self.db.Session.find({"date": date},
                                          {"course_name": 1,
                                           "teacher_name": 1,
                                           "interval_hour": 1
                                           })
            docs = list()
            for doc in cursor:
                del doc["_id"]
                docs.append(doc)
            self.write(json_encode(docs))
            self.finish()

        if request == "students":
            pass


def main():
    parse_command_line()
    http_server = HTTPServer(Application())
    http_server.listen(options.port, options.host)
    ioloop.IOLoop.instance().start()
    

if __name__ == "__main__":
    main()
