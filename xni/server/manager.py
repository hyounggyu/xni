import logging
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    pass

class MainHandler(BaseHandler):
    def get(self):
        self.write("Hello, world")

def main():
    app = tornado.web.Application(
        [
            (r'/', MainHandler),
        ],
    )
    app.listen('8000')
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
