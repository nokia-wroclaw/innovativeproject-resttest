import http.server
import urllib.parse
from threading import Thread, Timer
from time import sleep


class RequestHandler(object):
    def __init__(self, hostname, port, responses):
        self.hostname = hostname
        self.port = port
        resps = {}
        for name in responses:
            resps[name] = ExpirableResponse(name, name, responses[name].waittime, responses[name].status,
                                            responses[name].data)
        self.handler_class = _create_handler_class(resps)
        self.app = http.server.HTTPServer((hostname, port), self.handler_class)
        self.server_thread = Thread(target=self.app.serve_forever)

    def start(self):
        for key in self.handler_class.waiting_responses:
            self.handler_class.waiting_responses[key].set_expiration_function(self.handler_class.pop_response_by_name)
        for key in self.handler_class.waiting_responses:
            self.handler_class.waiting_responses[key].start_handling()
        self.server_thread.start()

    def join(self):
        while self.handler_class.waiting_responses:
            sleep(1)
        self.app.shutdown()
        self.server_thread.join()

    def get_responses(self):
        print(self.handler_class.expired_responses)
        return self.handler_class.expired_responses


class ExpirableResponse(object):
    def __init__(self, name, url, waittime, status, data):
        self.name = name
        self.waittime = waittime
        self.status = status
        self.data = data
        self.url = url
        self.timer = None
        self.handled = False
        pass

    def get_response_code(self):
        return self.status

    def get_headers(self):
        return {}

    def get_content(self):
        return str.encode(str(self.data))

    def match(self, path):
        return urllib.parse.urlparse(self.url).path == path

    def set_handled(self):
        self.handled = True
        self.timer.cancel()

    def set_expiration_function(self, func):
        self.timer = Timer(self.waittime, lambda: func(self.name))

    def start_handling(self):
        self.timer.start()


def _create_handler_class(resps):
    class DynamicHTTPHandler(http.server.BaseHTTPRequestHandler):
        waiting_responses = resps
        expired_responses = {}

        @classmethod
        def pop_response_by_name(cls, name):
            cls.expired_responses[name] = cls.waiting_responses.pop(name)
            return cls.expired_responses[name]

        @classmethod
        def pop_response_by_url(cls, url):
            for key in cls.waiting_responses:
                if cls.waiting_responses[key].match(url):
                    cls.expired_responses[key] = cls.waiting_responses.pop(key)
                    return cls.expired_responses[key]
            return None

        def do_GET(self):
            resp = self.pop_response_by_url(self.path)

            if resp is None:
                self.send_error(404, "URL <<" + self.path + ">> is not handled")
                return

            resp.set_handled()
            self.send_response(int(resp.get_response_code()))
            for key, value in resp.get_headers().items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(resp.get_content())

    return DynamicHTTPHandler
