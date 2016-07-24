import re
import traceback


class wsgiapp:
    """Base class for my wsgi application."""
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
        self.status = ''
        self.response_headers = []

    def header(self,name,value):
        self.response_headers.append((name,value))

    def delegate(self):
        print 'delegation start'
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']
        self.header('Content-type','text/plain')            
        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                # set the appropriate status
                self.status = '200 OK'
                # pass the matched groups as arguments to the function
                args = m.groups()
                funcname = method.upper() + "_" + name
                func = getattr(self, funcname)
                return func(*args)
        self.status = '404 NOT FOUND'            
        return self.notfound()

        
class myyapp(wsgiapp):
    urls = [
        ("/", "index"),
        ("/hello/(.*)", "hello"),
        ("/hello","index")
    ]

    def GET_index(self):
        self.start(self.status,self.response_headers)
        return "Hello World!\n"
    
    def GET_hello(self, name):
        self.start(self.status,self.response_headers)
        return "Hello %s!\n" % name

    def notfound(self):
        self.start(self.status,self.response_headers)
        return "Not Found\n"

def start_app(environ,start_response):
    return application(environ,start_response).delegate()
    