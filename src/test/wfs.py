"""
Unit tests for PCAPI WFS
"""

import os
import unittest

from pcapi.server import application
from pcapi import config

from webtest import TestApp

import xml.etree.ElementTree as ET


class TestWFS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestWFS, cls).setUpClass()
        cls.app = TestApp(application)
        cls.base_url = '/ows'

    def test_get_capabilities(self):
        # check invalid parameters
        resp = self.app.get(self.base_url).json
        self.assertEquals(resp['error'], 1)
        self.assertEquals(resp['msg'], 'No OWS SERVICE specified')

        service = 'XXX'
        url = '{0}?SERVICE={1}'.format(self.base_url, service)
        resp = self.app.get(url).json
        self.assertEquals(resp['error'], 1)
        self.assertEquals(
            resp['msg'],
            'Service {0} is not supported'.format(service))

        service = 'WFS'
        url = '{0}?SERVICE={1}'.format(self.base_url, service)
        resp = self.app.get(url).json
        self.assertEquals(resp['error'], 1)
        self.assertEquals(resp['msg'], 'ERROR: WFS version was not specified!')

        version = '0.1.0'
        url = '{0}?SERVICE={1}&VERSION={2}'.format(self.base_url, service, version)
        resp = self.app.get(url).json
        self.assertEquals(resp['error'], 1)
        self.assertEquals(
            resp['msg'],
            'WFS version {0} is not supported'.format(version))
        version = '1.1.0'
        url = '{0}?SERVICE={1}&VERSION={2}'.format(self.base_url, service, version)
        resp = self.app.get(url).json
        self.assertEquals(resp['error'], 1)
        self.assertEquals(resp['msg'], 'Request None is not supported')

        request = 'XXX'
        url = '{0}?SERVICE={1}&VERSION={2}&REQUEST={3}'.format(
            self.base_url, service, version, request)
        resp = self.app.get(url).json
        self.assertEquals(resp['error'], 1)
        self.assertEquals(resp['msg'], 'Request {0} is not supported'.format(request))

        # successful query, check cobweb:FeatureCollection1
        # is the name of the first FeatureType
        self.assertTrue(self._get_feature_types(1)[0].text.startswith('cobweb:'))

    def test_get_feature(self):
        def post_rec(url, name):
            with open(os.path.join(config.get("test", "test_resources"), name), "r") as f:
                resp = self.app.post(url, params=f.read()).json
                self.assertEquals(resp['error'], 0)

        gf_url = '{0}?SERVICE=WFS&VERSION=1.1.0&REQUEST=GETFEATURE'.format(
            self.base_url)

        resp = self.app.get(gf_url)
        self.assertEquals(resp.text, "Missing 'typeName'")

        type_name = 'XXX'
        url = '{0}&typename={1}'.format(gf_url, type_name)
        resp = self.app.get(url)
        self.assertEquals(
            resp.text,
            'featureType {0} not found in features.json'.format(type_name))

        uid = config.get("test", "test_uid")

        # post initial record to ensure test directory is setup
        rname = 'record1'
        r_url = '/records/local/{0}/{1}'.format(uid, rname)
        post_rec(r_url, 'testfile-sd1.rec')

        # delete all records
        self.app.delete('/records/local/{0}//'.format(uid)).json

        # test no records
        ft = self._get_feature_types(1)[0].text
        url = '{0}&typename={1}&OUTPUTFORMAT=json&test=1'.format(gf_url, ft)
        resp = self.app.get(url).json
        self.assertEquals(len(resp['features']), 0)

        # post a record for sd1
        post_rec(r_url, 'testfile-sd1.rec')
        url = '{0}&typename={1}&OUTPUTFORMAT=json&test=1'.format(gf_url, ft)
        resp = self.app.get(url).json
        self.assertEquals(len(resp['features']), 1)
        self.assertEquals(resp['features'][0]['properties']['fields'][0]['val'], 'val1')

        # gml
        url = '{0}&typename={1}&OUTPUTFORMAT&test=1'.format(gf_url, ft)
        resp = self.app.get(url)
        # TODO: missing template
        #print resp

        # post a record for sd2
        post_rec(r_url, 'testfile-sd2.rec')
        ft = self._get_feature_types(2)[0].text
        url = '{0}&typename={1}&OUTPUTFORMAT=json&test=1'.format(gf_url, ft)
        resp = self.app.get(url).json
        self.assertEquals(len(resp['features']), 1)
        self.assertEquals(resp['features'][0]['properties']['fields'][0]['val'], 'val2')

        # gml
        url = '{0}&typename={1}&OUTPUTFORMAT&test=1'.format(gf_url, ft)
        resp = self.app.get(url)
        # TODO: missing template
        #print resp

    # fetch feature type
    def _get_feature_types(self, type_i):
        request = 'GETCAPABILITIES'
        url = '{0}?SERVICE=WFS&VERSION=1.1.0&REQUEST=GETCAPABILITIES'.format(
            self.base_url)
        resp = self.app.get(url)
        namespaces = {'wfs': 'http://www.opengis.net/wfs'}
        root = ET.fromstring(resp.text)
        return root.findall('.//wfs:FeatureType[{0}]/wfs:Name'.format(type_i), namespaces)
