"""
Unit tests for PCAPI QA
"""

import os
import unittest

from pcapi import config
from pcapi.server import application

from webtest import TestApp

class TestQA(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestQA, cls).setUpClass()
        userid = 'testemail@domain.co.uk'
        provider = 'local'
        cls.REC_PREFIX = '/records/{0}/{1}'.format(provider, userid)
        cls.app = TestApp(application)

    def test_pip_filter(self):
        #  test point in polygon filter
        url = '{0}/'.format(self.REC_PREFIX)
        self.app.delete(url).json

        self._create_rec('rec_pos1')
        self._create_rec('rec_pos2')
        self._create_rec('rec_pos3')

        url = '{0}/'.format(self.REC_PREFIX)
        resp = self.app.get(url).json
        self.assertEquals(resp["error"], 0)
        self.assertEquals(len(resp['records']), 3)

        def check_filter(poly, count):
            resp = self.app.get(
                url,
                params={
                    'filter': 'pip',
                    'poly': poly
                    }
                ).json
            self.assertEquals(resp["error"], 0)
            self.assertEquals(len(resp['records']), count)

        check_filter('[[0,1.0],[1.0,1.0],[1.0,0],[0,0]]', 0)
        check_filter('[[0,10],[10,10],[10,0],[0,0]]', 1)
        check_filter('[[0,20],[20,20],[20,0],[0,0]]', 2)
        check_filter('[[-20,-20],[20,20],[20,20],[-20,20]]', 3)

        def check_error(poly, msg):
            resp = self.app.get(
                url,
                params={
                    'filter': 'pip',
                    'poly': poly
                    }
                ).json
            self.assertEquals(resp["error"], 1)
            self.assertEquals(resp['msg'], msg)

        err_msg = 'No JSON object could be decoded'
        check_error('', err_msg)
        check_error('[(0,1.0),(1.0,1.0),(1.0,0),(0,0)]', err_msg)

    def _create_rec(self, name):
        with open(os.path.join(
            config.get('test', 'test_resources'),
            'record_filter',
            '{0}.json'.format(name)), 'r') as f:
            url = '{0}/{1}'.format(self.REC_PREFIX, name)
            resp = self.app.post(url, params=f.read()).json
            self.assertEquals(resp["error"], 0)
