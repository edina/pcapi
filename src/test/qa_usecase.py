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

    def test_awr_filter(self):
        #  test attribute within range
        url = '{0}/'.format(self.REC_PREFIX)
        self.app.delete(url).json

        self._create_rec('rec_pos1')
        self._create_rec('rec_pos2')
        self._create_rec('rec_pos3')
        self._create_rec('rec_pos4')

        # test rangecheck with no max or min
        resp = self.app.get(
            url,
            params={
                'filter': 'rangecheck',
                'rangecheck_name': 'field-1'
            }
        ).json
        self.assertEquals(resp['msg'], 'Either rangecheck_min or rangecheck_max must be defined')
        self.assertEquals(resp['error'], 1)

        # test with no rangecheck_max
        def rangecheck_min(min, count):
            resp = self.app.get(
                url,
                params={
                    'filter': 'rangecheck',
                    'rangecheck_name': 'field-1',
                    'rangecheck_min': min
                }
            ).json
            self.assertEquals(len(resp['records']), count)
            self.assertEquals(resp['error'], 0)
        rangecheck_min(1.0, 3)
        rangecheck_min(2.1, 3)
        rangecheck_min(2.2, 2)
        rangecheck_min(4.0, 2)
        rangecheck_min(7.0, 0)

        # test with no rangecheck_min
        def rangecheck_max(max, count):
            resp = self.app.get(
                url,
                params={
                    'filter': 'rangecheck',
                    'rangecheck_name': 'field-1',
                    'rangecheck_max': max
                }
            ).json
            self.assertEquals(resp['error'], 0)
            self.assertEquals(len(resp['records']), count)
        rangecheck_max(1.0, 0)
        rangecheck_max(4.0, 2)
        rangecheck_max(7.0, 3)

        # test rangecheck_name missing
        resp = self.app.get(
            url,
            params={
                'filter': 'rangecheck',
                'rangecheck_min': '1',
                'rangecheck_max': '3'
            }
        ).json
        self.assertEquals(resp['error'], 1)
        self.assertEquals(resp['msg'], 'Parameter rangecheck_name must be specified')

        def check_error(min, max, msg):
            resp = self.app.get(
                url,
                params={
                    'filter': 'rangecheck',
                    'rangecheck_name': 'field-1',
                    'rangecheck_min': min,
                    'rangecheck_max': max
                }
            ).json
            self.assertEquals(resp["error"], 1)
            self.assertEquals(resp['msg'], msg)

        # test non float rangecheck variables
        check_error('notfloatmin', 3, 'could not convert string to float: notfloatmin')
        check_error(3, 'notfloatmax', 'could not convert string to float: notfloatmax')

        def rangecheck_min_max(min, max, count):
            resp = self.app.get(
                url,
                params={
                    'filter': 'rangecheck',
                    'rangecheck_name': 'field-1',
                    'rangecheck_min': min,
                    'rangecheck_max': max
                }
            ).json
            self.assertEquals(resp["error"], 0)
            self.assertEquals(len(resp['records']), count)

        # do some with both max and min defined queries
        rangecheck_min_max(0.0, 7, 3)
        rangecheck_min_max(3, 7.0, 2)
        rangecheck_min_max(3, 5, 1)
        rangecheck_min_max(2.1, 4, 2)
        rangecheck_min_max(4, 4, 1)

    def test_combined_pip_and_awr_filter(self):
        #  test combined point in polygon and attribute within range filter
        url = '{0}/'.format(self.REC_PREFIX)
        self.app.delete(url).json

        self._create_rec('rec_pos1')
        self._create_rec('rec_pos2')
        self._create_rec('rec_pos3')

        # will return rec_pos1 and rec_pos2
        poly = '[[0,20],[20,20],[20,0],[0,0]]'

        # range filter will only return rec_pos2
        resp = self.app.get(
            url,
            params={
                'filter': 'rangecheck,pip',
                'poly': poly,
                'rangecheck_name': 'field-1',
                'rangecheck_min': 3,
                'rangecheck_max': 5
            }
        ).json

        self.assertEquals(resp["error"], 0)
        records = resp['records']
        self.assertEquals(len(records), 1)
        self.assertEquals(records[0].keys()[0], 'rec_pos2')

        # will return rec_pos1, rec_pos2 and rec_pos3
        poly = '[[-20,-20],[20,20],[20,20],[-20,20]]'

        # range filter will only return rec_pos3
        resp = self.app.get(
            url,
            params={
                'filter': 'rangecheck,pip',
                'poly': poly,
                'rangecheck_name': 'field-1',
                'rangecheck_min': 6,
                'rangecheck_max': 7
            }
        ).json

        self.assertEquals(resp["error"], 0)
        records = resp['records']
        self.assertEquals(len(records), 1)
        self.assertEquals(records[0].keys()[0], 'rec_pos3')

    def _create_rec(self, name):
        with open(os.path.join(
            config.get('test', 'test_resources'),
            'record_filter',
            '{0}.json'.format(name)), 'r') as f:
            url = '{0}/{1}'.format(self.REC_PREFIX, name)
            resp = self.app.post(url, params=f.read()).json
            self.assertEquals(resp["error"], 0)
