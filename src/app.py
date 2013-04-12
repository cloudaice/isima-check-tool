#-*-coding: utf-8-*-
# @author: xiangchao<cloudaice@gmail.com>

import os
from lib import Mongo
#from tornado import gen
from tornado import web
from tornado import ioloop
from tornado.httpserver import HTTPServer
from tornado.options import define, parse_command_line, options


cnn = Mongo.conn()
db = cnn['isima']

define("port", default=8000, help='run on the given port', type=int)
define("host", default='127.0.0.1', help="run on the given host", type=str)


class Application(web.Application):
    def __init__(self):
        settings = {
            'static_path': os.path.join(os.path.dirname(__file__), 'static'),
            'template_path': os.path.join(os.path.dirname(__file__), 'template'),
            'debug': True
        }

        handlers = [
            (r'/', Home),
            (r'/about', About),
            (r'/contact', Contact),
            (r'/login', Login),
            (r'/favicon.ico', web.StaticFileHandler, dict(path=settings['static_path'])),
        ]

        web.Application.__init__(self, handlers, **settings)

class BaseHandler(web.RequestHandler):
    def get_current

class Home(web.RequestHandler):
    def get(self):
        self.render('home.html')
    
    def post(self):
        pass


class About(web.RequestHandler):
    def get(self):
        self.render('about.html')


class Contact(web.RequestHandler):
    def get(self):
        self.render('home.html')


class Login(web.RequestHandler):
    def get(self):
        self.render('login.html')




def main():
    parse_command_line()
    http_server = HTTPServer(Application())
    http_server.listen(options.port, options.host)
    ioloop.IOLoop.instance().start()
    

if __name__ == "__main__":
    main()
