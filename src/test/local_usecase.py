# -*- coding: utf-8 -*-
"""
Local provider use-case for FTGB tests. This is not coverage-test but use-case
testing -- Authoring tool / ftgb use case used for demonstrating fieldtrip-open

Local provider has no oauth implementation yet. User will just need to:
1. Use an e-mail address as USERID. Whoever has the user's email has access.
2. PUT/POST before "reading" anything. No user directory is created unless
   something is uploaded.
"""
import base64
import os
import sys
import unittest

from webtest import TestApp

## Also libraries to the python path
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(pwd, '../'))  # to find the classes to test

from pcapi.server import application
from pcapi import config

userid = "testemail@domain.co.uk"
textfilepath = config.get("test", "testfile")
imagefilepath = config.get("test", "imagefile")
editorfilepath = config.get("test", "editorfile")

# a record file (json)
localfile = open ( textfilepath , "r")
# am editor file (html5)
editorfile = open ( editorfilepath , "r")

# Application
app = TestApp(application)
provider = 'local'

class TestAuthoringTool(unittest.TestCase):
    """
    Test initial creation with authoring tool:
    Get all editors:
        /editors/local/testemail@domain.com/

    Get all records:
        /records/local/testemail@domain.com/

    Get one record:
        /records/local/testemail@domain.com/testtt

    Get one editor:
        /editors/local/testemail@domain.com/cobweb.edtr

    Get one image:
        /records/local/testemail@domain.com/testtt/1385980310970.jpg

    Update am image(PUT req):
        /records/local/testemail@domain.com/testtt

    Delete record (DELETE):
        /records/local/testemail@domain.com/123

    Sync:
        /sync/local/testemail@domain.com

        /sync/local/testemail@domain.com/123456789

    Post mbtiles/kml (POST):
        /features/local/testemail@domain.com/dyfi.mbtiles
    """
    ########### GET EDITORS ###########

    def test_post_editor(self):
        """  post an editor """

        url='/fs/{0}/{1}/editors/test.json'.format(provider,userid)
        editor = editorfile.read()
        with open (os.path.join(config.get("test", "test_resources"), 'form.json'), "r") as f:
            resp = app.post(url, params=f.read()).json
            self.assertEquals(resp["error"], 0 )
        # Contents of /editors/ should be the "/editors/test.json" (always receives absolute paths)
        resp = app.get('/fs/{0}/{1}/editors'.format(provider,userid) ).json
        #print `resp`
        self.assertTrue("/editors/test.json" in resp["metadata"])


    def test_get_all_editors(self):
        """  Get all Editors """
        self.test_post_editor() #prereq
        url='/editors/{0}/{1}/'.format(provider,userid)
        resp = app.get(url).json
        self.assertEquals(resp["error"], 0 )
        try:
            self.assertTrue("test.json" in resp["metadata"])
            self.assertTrue("test-form" in resp["names"])
        except:
            print "Assertion failed. Got: %s" % `resp`
    ########### GET RECORDS ###########

    def test_post_record(self):
        """  post an editor """
        url='/fs/{0}/{1}/records/test/record.json'.format(provider,userid)
        resp = app.post(url, params=localfile.read() ).json
        self.assertEquals(resp["error"], 0 )
        # Contents of /records/ should be the "/records/test/record.json"
        resp = app.get('/fs/{0}/{1}/records/test'.format(provider,userid) ).json
        self.assertTrue("/records/test/record.json" in resp["metadata"])


    def test_get_all_records(self):
        """ IMPORTANT: Deletes records, posts 2 name-coliding records and returns all records!"""
        #cleanup EVERYTHING under /records/
        url = '/records/{0}/{1}//'.format(provider,userid)
        app.delete(url).json

        # create myrecord/record.json
        url = '/records/{0}/{1}/myrecord'.format(provider,userid)
        resp = app.post(url, upload_files=[("file" , textfilepath )] ).json
        self.assertEquals(resp["error"], 0)
        self.assertEquals(resp["path"], "/records/myrecord/record.json")
        # create myrecord (1)record.json
        url = '/records/{0}/{1}/myrecord'.format(provider,userid)
        resp = app.post(url, upload_files=[("file" , textfilepath )] ).json
        self.assertEquals(resp["error"], 0)
        # auto-renamed!
        self.assertEquals(resp["path"], "/records/myrecord (1)/record.json")
        #get all records
        url = '/records/{0}/{1}/'.format(provider,userid)
        resp = app.get(url).json
        self.assertEquals(resp["error"], 0)
        #print len ( resp["records"] )
        self.assertEquals(len ( resp["records"] ) , 2 )

    def test_filter_records(self):
        #  test record filter
        url = '/records/{0}/{1}//'.format(provider, userid)
        app.delete(url).json

        def create_rec(name):
            with open(os.path.join(
                config.get('test', 'test_resources'),
                'record_filter',
                '{0}.json'.format(name)), 'r') as f:
                url = '/records/{0}/{1}/{2}'.format(provider, userid, name)
                resp = app.post(url, params=f.read()).json
                self.assertEquals(resp["error"], 0)

        create_rec('rec1_ed1')
        create_rec('rec2_ed1')
        create_rec('rec3_ed2')

        url = '/records/{0}/{1}/'.format(provider,userid)
        resp = app.get(url).json
        self.assertEquals(resp["error"], 0)
        self.assertEquals(len(resp['records']), 3)

        def check_editor_filter(name, count):
            resp = app.get(
                url,
                params={
                    'filter': 'editor',
                    'id': name
                }
            ).json
            self.assertEquals(resp["error"], 0)
            self.assertEquals(len(resp['records']), count)

        check_editor_filter('xxx', 0)
        check_editor_filter('ed1.json', 2)
        check_editor_filter('ed2.json', 1)

    def test_get_invalid_records(self):
        url = '/records/{0}/{1}//'.format(provider, userid)
        app.delete(url).json

        # post invalid record
        url = '/records/{0}/{1}/myrecord'.format(provider, userid)
        with open (os.path.join(config.get("test", "test_resources"), 'invalid.rec'), "r") as f:
            resp = app.post(url, params=f.read()).json
            self.assertEquals(resp["error"], 0 )

        url = '/records/{0}/{1}/'.format(provider, userid)
        resp = app.get(url).json

        # get all returns 0 but no error
        self.assertEquals(len(resp["records"]), 0)
        self.assertEquals(resp["error"], 0)

    #### FILES ####

    def test_fs_file_upload(self):
        """ FS all Records"""
        # put first file at /lev1/lev2 with content: "Hello World!\n"
        #print "test_get_file"
        contents = "Hello World!\n"
        url='/fs/{0}/{1}/lev1/lev2 with spaces'.format(provider,userid)
        resp = app.put(url, params=contents ).json
        self.assertEquals(resp["error"], 0 )
        # Contents of GET should be the same
        resp = app.get('/fs/{0}/{1}/lev1/lev2 with spaces'.format(provider,userid) )
        self.assertEquals(resp.body , contents)

    def test_delete_file(self):
        """ DELETE on /fs/ path deletes the file or directory """
        #print "test_delete_file"
        # put first file at /lev1/lev2
        resp = app.put('/fs/{0}/{1}/lev1/lev2'.format(provider,userid), params=localfile.read() ).json
        self.assertEquals(resp["error"], 0 )
        # Now delete it
        resp = app.delete('/fs/{0}/{1}/lev1/lev2'.format(provider,userid) ).json
        self.assertEquals(resp["error"], 0 )

    def test_create_sync(self):
        """Get Cursor before adding a file, then sync to see the changes made"""
        #cleanup EVERYTHING under /records/
        url = '/records/{0}/{1}//'.format(provider,userid)
        app.delete(url).json
        # get cursor
        cur_resp = app.get('/sync/{0}/{1}'.format(provider,userid)).json
        #print "cursor is " + `cur_resp`
        #create new record
        url = '/records/{0}/{1}/myrecord'.format(provider,userid)
        put_resp = app.post(url, params=localfile.read() ).json
        self.assertEquals(put_resp["error"], 0)
        # get diffs
        url = '/sync/{0}/{1}/{2}'.format(provider,userid,cur_resp["cursor"])
        diff_resp = app.get(url).json
        self.assertEquals( diff_resp["updated"] , [u'/records/myrecord/record.json'] )

    @unittest.skip("WIP test_public_editors_layers")
    def test_editors_interface(self):
        """ This is to test the new /editors/ -> /fs/ schema as described in
        https://github.com/cobweb-eu/cobweb/issues/166
        """
        # Post editor
        ## /editors/local/UUID/SID/XXX -> /SID/records/NAME/record.json
        editor = editorfile.read()
        SID = "BADBEEF"
        extra_resource = localfile.read() #eg an image or Decision Tree

        url='/editors/{0}/{1}/{2}'.format(provider,userid,SID)
        resp = app.put(url, params=editor).json
        url='/editors/{0}/{1}/{2}'.format(provider,userid,SID)
        resp = app.put(url, params=extra_resource).json

    #@unittest.skip("skipping test")
    def test_public_editors_layers(self):
        """  Put an overlay and an editor with public=true and see if they are copied
        over to the public folder"""

        # create public layer mylayer.
        layer = localfile.read()
        # NOTE: public=true
        url='/features/{0}/{1}/mylayer.kml?public=true'.format(provider,userid)
        resp = app.put(url, params=layer).json
        self.assertEquals(resp["error"], 0 )
        ## The same with editor
        editor = editorfile.read()
        # NOTE: public=true
        url='/editors/{0}/{1}/mylayer.kml?public=true'.format(provider,userid)
        resp = app.put(url, params=editor).json


class TestMobileApp(unittest.TestCase):
    def test_image_upload(self):
        url = '/records/{0}/{1}//'.format(provider, userid)
        app.delete(url).json

        # create new record
        rname = 'myrecord'
        url = '/records/{0}/{1}/{2}'.format(provider, userid, rname)
        resp = app.post(url, params=localfile.read()).json
        self.assertEquals(resp['error'], 0)

        # post binary image
        bfname = 'image.jpg'
        resp = app.post('{0}/{1}'.format(url, bfname),
                        upload_files=[('file' , imagefilepath)] ).json
        self.assertEquals(resp['error'], 0)
        self.assertEquals(resp['msg'], 'File uploaded')
        self.assertEquals(resp['path'], '/records/{0}/{1}'.format(rname, bfname))

        # post base64 string (based on encoding of test image)
        sfname = 'imageb64.jpg'
        with open(imagefilepath, 'r') as f:
            out = base64.b64encode(f.read())
            resp = app.post('{0}/{1}?base64=true'.format(url, sfname), params=out).json
            self.assertEquals(resp['error'], 0)
            self.assertEquals(resp['msg'], 'File uploaded')
            self.assertEquals(resp['path'], '/records/{0}/{1}'.format(rname, sfname))

        # verify both files have same size
        d = os.path.join(config.get("path", 'data_dir'), userid, 'records', rname)
        self.assertEquals(
            os.stat(os.path.join(d, bfname)).st_size,
            os.stat(os.path.join(d, sfname)).st_size)
