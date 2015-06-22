# WebTestMixin
# https://github.com/NoyaInRain/util/blob/master/webtest.py
# by Sven James <sven.jms AT gmail.com>
# released into the public domain

"""Tornado test mixin that provides a HTTP web server/app.

Some simple `RequestHandler`s for serving resources are included with the
module.
"""

# Python forward compatibility
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

from tornado.web import Application, RequestHandler
from tornado.httpserver import HTTPServer

class WebTestMixin(object):
    """Subclass API: `AsyncTestCase` mixin that provides a HTTP web server/app.

    `RequestHandler`s can be added to the `webapp` property, as usually with
    `add_handlers()`. Tornado comes with some useful handlers for testing (e.g.
    `ErrorHandler`) and some more are included with this module.

    Make sure to call both `setUp()` and `tearDown()`.

    Attributes:

    * `webapp`: Tornado `Application`.
    * `webapp_url`: URL under which web app is available.
    * `webserver`: local Tornado `HTTPServer` which serves `webapp`.
    """

    def setUp(self, port=16080):
        """Set up `WebTestMixin`.

        The web server will listen on the given `port`. If initializing the
        server fails, an `IOError` is raised.
        """
        self.webapp = Application()
        self.webapp_url = 'http://localhost:{}/'.format(port)
        self.webserver = HTTPServer(self.webapp)
        self.webserver.listen(port)

    def tearDown(self):
        self.webserver.stop()

class SimpleResource(RequestHandler):
    """Request handler which simply serves a given string.

    The handler accepts two keyword arguments: `content` is the content to be
    delivered. `content_type` is the corresponding media type.
    """

    def initialize(self, content, content_type):
        self.content = content
        self.content_type = content_type

    def get(self):
        self.set_header('Content-Type', self.content_type)
        self.write(self.content)

class FileResource(RequestHandler):
    """Request handler which serves a file.

    The handler accepts two keyword arguments: `path` is the path to the file to
    be delivered. `content_type` is the corresponding media type.

    If there is a problem reading the file, HTTP error 500 is returned.
    """

    def initialize(self, path, content_type):
        self.path = path
        self.content_type = content_type

    def get(self):
        try:
            self.set_header('Content-Type', self.content_type)
            with open(self.path, 'rb') as f:
                self.write(f.read())
        except IOError:
            self.send_error()
