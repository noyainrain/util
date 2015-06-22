# WebTestMixin
# https://github.com/NoyaInRain/util/blob/master/webtest.py
# by Sven James <sven.jms AT gmail.com>
# released into the public domain

# Python forward compatibility
from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import os
from tornado.httpclient import HTTPError
from tornado.testing import AsyncTestCase, AsyncHTTPClient, gen_test
from webtest import WebTestMixin, SimpleResource, FileResource

RES_PATH = os.path.join(os.path.dirname(__file__), 'res')

class WebTestMixinTest(AsyncTestCase, WebTestMixin):
    def setUp(self):
        super(WebTestMixinTest, self).setUp()
        WebTestMixin.setUp(self)

    def tearDown(self):
        WebTestMixin.tearDown(self)
        super(WebTestMixinTest, self).tearDown()

    @gen_test
    def test_get(self):
        self.webapp.add_handlers('', [
            ('/$', SimpleResource,
             {'content': 'Meow!', 'content_type': 'text/plain'})
        ])
        response = yield AsyncHTTPClient().fetch(self.webapp_url)
        self.assertEqual(response.headers.get('Content-Type'), 'text/plain')
        self.assertEqual(response.body, 'Meow!')

    @gen_test
    def test_get_file_resource(self):
        self.webapp.add_handlers('', [
            ('/$', FileResource, {
                'path': os.path.join(RES_PATH, 'webtest.txt'),
                'content_type': 'text/plain'
            })
        ])
        response = yield AsyncHTTPClient().fetch(self.webapp_url)
        self.assertEqual(response.headers.get('Content-Type'), 'text/plain')
        self.assertEqual(response.body, 'Meow!\n')

    @gen_test
    def test_get_file_resource_nonexisting_path(self):
        self.webapp.add_handlers('', [
            ('/$', FileResource, {'path': 'foo', 'content_type': 'foo'})
        ])
        with self.assertRaises(HTTPError):
            yield AsyncHTTPClient().fetch(self.webapp_url)
