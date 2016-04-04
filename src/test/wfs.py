"""
Unit tests for PACPI WFS
"""

import unittest

from pcapi.server import application
from webtest import TestApp

import xml.etree.ElementTree as ET

class TestWFS(unittest.TestCase):
    def test_get_capabilities(self):
        app = TestApp(application)
        base_url='/ows'

        # check invalid parameters
        resp = app.get(base_url).json
        self.assertEquals(resp['error'], 1)
        self.assertEquals(resp['msg'], 'No OWS SERVICE specified')

        service = 'XXX'
        url = '{0}?SERVICE={1}'.format(base_url, service)
        resp = app.get(url).json
        self.assertEquals(resp['error'], 1)
        self.assertEquals(
            resp['msg'],
            'Service {0} is not supported'.format(service))

        service = 'WFS'
        url = '{0}?SERVICE={1}'.format(base_url, service)
        resp = app.get(url).json
        self.assertEquals(resp['error'], 1)
        self.assertEquals(resp['msg'], 'ERROR: WFS version was not specified!')

        version = '0.1.0'
        url = '{0}?SERVICE={1}&VERSION={2}'.format(base_url, service, version)
        resp = app.get(url).json
        self.assertEquals(resp['error'], 1)
        self.assertEquals(
            resp['msg'],
             'WFS version {0} is not supported'.format(version))

        version = '1.1.0'
        url = '{0}?SERVICE={1}&VERSION={2}'.format(base_url, service, version)
        resp = app.get(url).json
        self.assertEquals(resp['error'], 1)
        self.assertEquals(resp['msg'], 'Request is not defined')

        request = 'XXX'
        url = '{0}?SERVICE={1}&VERSION={2}&REQUEST={3}'.format(
            base_url, service, version, request)
        resp = app.get(url).json
        self.assertEquals(resp['error'], 1)
        self.assertEquals(resp['msg'], 'Request {0} is not supported'.format(request))

        # successful query, check cobweb:FeatureCollection1
        # is the name of the first FeatureType
        request = 'GETCAPABILITIES'
        url = '{0}?SERVICE={1}&VERSION={2}&REQUEST={3}'.format(
            base_url, service, version, request)
        resp = app.get(url)
        namespaces = {'wfs': 'http://www.opengis.net/wfs'}
        root = ET.fromstring(resp.text)
        ft = root.findall('.//wfs:FeatureType[1]/wfs:Name', namespaces)
        self.assertEquals(ft[0].text, 'cobweb:FeatureCollection1')
