#-*-coding: utf-8-*-
# @author: xiangchao<cloudaice@gmail.com>

import sys
import os
from lib import Mongo
#from tornado import gen
from tornado import web
from tornado import ioloop
from tornado.httpserver import HTTPServer
#from tornado.escape import json_encode

cnn = Mongo.conn()
db = cnn['isima']


class Home(web.RequestHandler):
    def get(self):
        self.render('home.html')
    
    def post(self):
        pass

settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'template'),
    'debug': True
}


application = web.Application([(r'/', Home),
                               (r'/favicon.ico', web.StaticFileHandler,
                                   {'path': settings['static_path']}),
                               ], **settings
                              )


if __name__ == "__main__":
    port = int(sys.argv[1])
    http_server = HTTPServer(application)
    http_server.listen(port, '127.0.0.1')
    ioloop.IOLoop.instance().start()
