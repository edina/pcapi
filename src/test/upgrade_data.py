# -*- coding: utf-8 -*-
"""
Convert existing records to the new format where the id does not contain
fieldcontain

Test Process:
1) Upload a few test records from the ENVSYS test-data
2) Export to PostGIS

"""
import os
import sys
import json
import unittest

from webtest import TestApp

## Also libraries to the python path
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(pwd, '../'))  # to find the classes to test

from pcapi.server import application
from pcapi import config
from pcapi.utils.pcapi_upgrade import find_json, updateIdExtensionInGeojson, updateEditorExtension

userid = "testexport@domain.co.uk"

# where to get records ala "recordXXX.json" from
envsys_records_dir = config.get("test", "records_dir")
# How many records
records_num = 15

# Application
app = TestApp(application)
provider = 'local'

class TestUpgrade(unittest.TestCase):
    """
    open a record and check if id has been updated
    """
    ########### UPLOAD RECORDS ###########

    def test_updateIdExtensionInGeojson(self):
        """ read a geojson and check if id has been updated"""
        gen = find_json(envsys_records_dir)
        record = json.load(open(gen.next()))
        new_record = updateIdExtensionInGeojson(record)
        self.assertEquals(new_record["properties"]["fields"][0]["id"],
            record["properties"]["fields"][0]["id"].replace("fieldcontain-", ""))
        self.assertEquals(new_record["properties"]["fields"][0]["type"],
            record["properties"]["fields"][0]["id"].split("-")[0])

    def test_updateEditorExtension(self):
        """ read geojson and check if editor extension has changed"""
        gen = find_json(envsys_records_dir)
        record = json.load(open(gen.next()))
        new_record = updateEditorExtension(record)
        self.assertEquals(new_record["properties"]["editor"],
            record["properties"]["editor"].replace(".edtr", ".json"))
