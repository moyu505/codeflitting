# -*- coding: UTF-8 -*-
import time
import json
import torndb
import tornado.wsgi, tornado.httpserver
from jinja2 import Environment, FileSystemLoader
from setting import *
from markdown2 import Markdown
class Application(tornado.wsgi.WSGIApplication):
    def __init__(self):
        handlers = [(r"/", HomePage),
                    (r'/login', LoginHandler),
                    (r'/test', TestHandler),
                    (r'/logout', LogoutHandler),
                    (r'/write', WriteHandler),
                    (r'/article', ArticleHandler),
                    (r'/register', RegisterHandler)
                    ]
        settings = dict(
            cookie_secret='S6Bp2cVjSAGFXDZqyOh+hfn/fpBnaEzFh22IVmCsVJQ=',
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            login_url='/login',
            # xsrf_cookies=True,
            )
        tornado.wsgi.WSGIApplication.__init__(self, handlers, **settings)
        self.env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'),encoding='utf-8'))
        self.db = torndb.Connection(
                            host=MYSQL_HOST, database=MYSQL_DB,
                            user=MYSQL_USER, password=MYSQL_PASS,
                            max_idle_time=30)
class BaseHandler(tornado.web.RequestHandler):
    """"""
    @property
    def db(self):
        return self.application.db;

    def get_current_user(self):
        return self.get_secure_cookie('username')

    def render(self, templates, parameter=dict()):
        self.write(self.application.env.get_template(templates).render(parameter))


class TestHandler(BaseHandler):
    """"""
    def get(self):
        cookie_dict = {}
        func = self.get_argument('callback')
        cookie_dict['cookie'] = self.get_cookie("username")
        res  = func + '(' + json.dumps(cookie_dict) + ')'
        self.set_header('Content-Type', 'application/javascript')
        self.set_header("Access-Control-Allow-Origin", "http://www.baidu.com")
        self.set_header("Access-Control-Allow-Credentials", True)
        self.redirect("/")
        print res
        self.write(res)

class HomePage(BaseHandler):
    """"""
    def get(self):
        category = self.get_argument('category', '')
        tag = self.get_argument('tag','')
        parameter = {}
        parameter['username'] = self.current_user
        parameter['infos'] = []
        parameter[category] = 'active'

        sql = "select * from pycoder_post where category like '%%%%%s%%%%' AND tag like '%%%%%s%%%%' ORDER BY timestamp DESC" % (category, tag)
        article_info = self.db.query(sql)
        for info in article_info:
            infos = "%s:%s:%s:%s" % (info['id'], info['title'], info['tag'], info['category'])
            parameter['infos'].append(infos)

        self.render('base.html', parameter)

class ArticleHandler(BaseHandler):
    """"""
    def get(self):
        parameter = {}
        markdowner = Markdown(extras=['wiki-tables','fenced-code-blocks'])
        parameter['username'] = self.current_user
        article_id = self.get_argument('id')
        sql = "select * from pycoder_post where id=%s" % article_id
        article_info = self.db.query(sql)[0]
        parameter['title'] = article_info['title']
        parameter['content'] = markdowner.convert(article_info['html'])
        times = time.localtime(int(article_info['timestamp']))
        parameter['edit_time'] = time.strftime("%Y-%m-%d %H:%M:%S", times)
        self.render('article.html', parameter)

class WriteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        parameter = {}
        parameter['username'] = self.current_user
        self.render('write.html', parameter)

    def post(self):
        title = self.get_argument('title')
        if title == "":
            self.redirect('/write')
            return
        tag = self.get_argument('tag')
        category = self.get_argument('category')
        content = self.get_argument('content')
        timestamp = str(int(time.time()))
        self.db.execute("insert into pycoder_post(title, tag, category, html, timestamp) values('%s', '%s', '%s', '%s', %s)" % (title, tag, category, content, timestamp));
        self.redirect('/')


class RegisterHandler(BaseHandler):
    def get(self):
        self.render('sign.html', {'sign':"Sign up"})

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        user_info = self.db.query("select username, password from pycoder_user")
        for info in user_info:
            if username == info['username']:
                self.redirect('/register')
                return
        #self.db.execute("insert into pycoder_user (username, password) values ('%s', '%s')" % (username,password))
        self.redirect('/login')

class LoginHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render('sign.html', {'sign':'Sign in'})

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        user_info = self.db.query("select username, password from pycoder_user")
        for info in user_info:
            if username == info['username'] and password == info['password']:
                self.set_secure_cookie('username', username)
                self.redirect('/')
                return
        self.redirect('/login')

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('username')
        self.redirect('/')

if 'SERVER_SOFTWARE' in os.environ:
    from bae.core.wsgi import WSGIApplication
    application = WSGIApplication(Application())
else:
    if __name__ == '__main__':
    #    tornado.options.parse_command_line()
        #创建一个服务器
        http_server = tornado.httpserver.HTTPServer(tornado.wsgi.WSGIContainer(Application()))
        #监听端口
        http_server.listen(8080)
        #启动服务
        tornado.ioloop.IOLoop.instance().start()
