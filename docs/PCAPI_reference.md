<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**
<!-- *generated with [DocToc](https://github.com/thlorenz/doctoc)*-->

- [Personal Cloud API](#personal-cloud-api)
- [Introduction](#introduction)
- [API Calls](#api-calls)
  - [Storage Providers:](#storage-providers)
    - [Filesystem](#filesystem)
    - [Delete a file with HTTP DELETE](#delete-a-file-with-http-delete)
    - [List files in folder](#list-files-in-folder)
    - [Get (and optionally transform) an individual media asset from a specified folder](#get-and-optionally-transform-an-individual-media-asset-from-a-specified-folder)
  - [EDITOR/RECORD access](#editorrecord-access)
    - [Get editors in Folder](#get-editors-in-folder)
    - [Get all records](#get-all-records)
    - [Get one record/editor](#get-one-recordeditor)
      - [for an editor](#for-an-editor)
      - [for a record:](#for-a-record)
    - [Create a record with POST](#create-a-record-with-post)
    - [Upload an editor (aka survey)](#upload-an-editor-aka-survey)
    - [Delete record](#delete-record)
    - [Publish record to PostGIS and (optionally) a Geoserver W*S endpoint](#publish-record-to-postgis-and-optionally-a-geoserver-ws-endpoint)
    - [Synchronize records](#synchronize-records)
    - [Synchronization example:](#synchronization-example)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Personal Cloud API
===================

# Introduction

This the API specification for the Personal Cloud
middleware. This document is constantly updated to reflect the master branch. Considerable effort is always undertaken to avoid breaking existing API when developing new features.

The following assumptions were made:

Its main purpose is to act as a middleware for the EDINA mobile
Fieldtrip open app but can be used as a standalone storage container.

It should generally provide all facilities that are not implementable at
the client-side due to portability, processing power, storage and
framework limitations of a mobile phone

Its main functions are to store, process and deliver data sent by a mobile phone using **an extremely lightweight and versatile API** that allows a high degree of control without sacrificing usability.

The API is purely REST based and leverages most of the HTTP operations
(including PUT, DELETE etc.). All API calls are meant to be
generic and compatible with both a command line HTTP client
like `curl` as well as a browser-based `XMLHttpRequest` client.

The Application Programming Interface (API) described here
relates to the web service “PC API” available at the default endpoint:

https://localhost:8080/pcapi/

NOTE:

A Secure transport protocol (SSLv3/TLS) is strongly recommended for all
communications. PCAPI itself will work exactly the same in both HTTP and HTTPS.

# API Calls

## Storage Providers:

A simple GET request that returns a list of all supported
storage providers together with their capabilities as json:

```bash
$ curl localhost:8080/1.3/pcapi/auth/providers
```

Will return something similar to:

```JSON
{
"edina": ["search", "synchronize", "delete"],
"dropbox" : ["oauth", "search", "synchronize", "delete"],
"googledrive" : ["oauth", "search", "synchronize", "delete"]
}
```

### Filesystem

The URL pattern used for filesystem access is as follows:

`fieldtripgb.edina.a.cuk/1.3/fs/<PROVIDER>/<USERID>/<PATH>`

Where:

**PROVIDER**

The storage provider to use

**USERID**

A token that allows the user to authenticate. This is provider
dependent and is generated from the provider’s equivalent
tokens (e.g. oAuth access tokens). See authentication.

**PATH**

The relative filesystem path pointing to a file or folder which
will be appended to the user’s sandbox

For example, to create a file with HTTP PUT (overwrite) or POST (create)

```bash
curl -X PUT -T myfile
localhost:8080/1.3/pcapi/fs/dropbox/userid/myDirectory/myfilename
```

All intermediate directories are created on the fly e.g. if
myDirectory does not exist it will be created.

`PUT` requests should place all file contents inside the body of
the request. If the target file already exists it will be
overwritten.

When `POST`ing a file, the file contents must be sent as
*multipart/form-data* inside a field named file. This is done for
compatibility with *Cordova*. If a file with the same name
already exists, then the uploaded file will be saved under a
different name. The new name is in the value of the path
property.

Example with POST:

```bash
curl -X POST --form file=@somefile
localhost:8080/1.3/pcapi/fs/dropbox/userid/myDirectory/myfilename
```

Sample reponse:

```JSON
{ "error": 0, "msg" : "File uploaded", "path": "/mydir/file
(2).txt" }
```

### Delete a file with HTTP DELETE

```bash
curl -X DELETE
localhost:8080/1.3/pcapi/fs/dropbox/userid/myDirectory/myfilename
```

### List files in folder

List files using GET

```bash
curl localhost:8080/1.3/pcapi/fs/dropbox/userid/myDirectory
```

NOTE: Directories are now automatically probed (no need for a trailing
slash).

### Get (and optionally transform) an individual media asset from a specified folder

A simple GET request pointing to the file will download it in
its original format.

```bash
curl
localhost:8080/1.3/pcapi/fs/dropbox/userid/myDirectory/myfilename?format=jpeg&dimensions=80,80
```

If the asset is an image file then the optional arguments format
and dimensions will attempt to convert the asset to the
specified format and dimensions before downloading:

e.g.

```bash
curl
localhost:8080/1.3/pcapi/fs/dropbox/userid/myDirectory/myfilename?format=jpeg&dimensions=80,80
```

## EDITOR/RECORD access

The URL pattern used for accessing editors and records should
start with /editors or /records respectively. E.g.

`localhost:8080/1.3/pcapi/editors/<PROVIDER>/<USERID>/<PATH>``

The PATH convention used is as follows:

Each record has its own folder named after the record "name".

All editors are in one big folder.

### Get editors in Folder

A simple GET request will return all editors with the default
".edtr" extension in the metadata property. Furthermore all
editor files will be parsed for a survey title which will be
added to the names property. If the parsing fails (no title,
unsupported editor format etc.) then javascript's null will be
used instead:

```bash
curl localhost:8080/1.3/pcapi/editors/local/userid/
```

Example Output:

```JSON
{
"metadata": [
"/editors/ddddd.edtr",
"/editors/eeee.edtr",
"/editors/test.edtr",
"/editors/trees.edtr"
],
"names": [
"Survey 1",
"My Survey Title"
"Another title"
null
],
"error": 0
}
```

### Get all records

A simple GET request returns all record files as a JSON array:

```bash
curl localhost:8080/pcapi/records/dropbox/userid
```

The optional filter argument will filter the returned list of
records based on the following values:

Where:

**attribute**

Filter on attribute. Return list of records that contain an attribute with the specified value. Example:

```
filter=attribute&attribute_name=description&attribute_value=My%20Survey

All parameters are mandatory.

```

**editor**

Filter based on editor id using the format `filter=editor&id=myeditor.edtr`

**envelope**

Filter based on bounding box parameter bbox using the format
filter=envelope&bbox=<xmin>, <ymin>, <xmax>,<ymax>

**date**

Filter based on a date range defined by parameters start_date
and end_date. The end_date is optional and will default to the
current time if omitted. Example:

`filter=date&start_date=20121101_12:00:00&end_date=20121105_12:00:00`

**format**

Return geodata in a specific format, either GeoJSON, KML or CSV.

`filter=format&frmt=geojson`

Additionally, the special parameter frmt=database will export all
data to a preconfigured PostGIS database according to the values
of ./etc/config.ini.

**mimetype**

Filter on mime type of media format

NOTE: Currently implemented filters are envelope, editor, format and
date.

Example Output:

```JSON
{
    "records": [{
        "duncan st": {
        "fields": [{
            "id": "fieldcontain-image-1",
            "val": "1366031020249.jpg",
            "label": "Take"
            }],
        "point": {
            "lat": 55.93561960435346,
            "alt": null,
            "lon": -3.1763742274678237
        },
            "editor": "litter in edinburgh.edtr",
            "timestamp": "2013-04-15T13:04:00.464Z",
            "name": "duncan st"
        }
    },
    {
        "desk (5)": {
        "fields": [{
            "id": "fieldcontain-image-1",
            "val": "1365757260427.jpg",
            "label": "Image"
            }],
        "name": "desk (5)",
        "editor": "image.edtr",
        "timestamp": "2013-04-12T09:01:18.840Z",
        "point": {
            "lat": 55.93749020527392,
            "alt": null,
            "lon": -3.1780926655209907
            }
        }
    }],
    "error": 0
}
```

**pip**

Point in polygon filter. Return list of records whose point is within the bounds of the specified polygon. Example:

```
filter=pip&poly=[[0,0], [0,2], [2,2], [2,0]]
```

**rangecheck**

Attribute within range filter.  Return list of records that contains an attribute value within the defined range. Example:

```
filter=rangecheck&rangecheck_name=height&rangecheck_min=1&rangecheck_max=2
```

Mandatory values are `rangecheck_name` and at least on `rangecheck_`.

### Get one record/editor

This is an example of having a GET request in order to get back
a single record or editor:

#### for an editor

```bash
curl localhost:8080/1.3/pcapi/editors/dropbox/userid/editor.edtr
```

Example output:

```html
<form id="form532" data-ajax="false">
    <div class="fieldcontain" id="fieldcontain-text-1">
        <label for="form-text-1">Title</label>
        <input name="form-text-1" id="form-text-1" type="text"
        required="" placeholder="record name" maxlength="15">
    </div>
    <div class="fieldcontain" id="fieldcontain-radio-1">
        <fieldset data-role="controlgroup">
        <legend>Choose</legend>
        <label for="form-radio-1">Happy</label>
        <input name="form-radio1" id="form-radio-1" value="Happy"
        type="radio" required="">
        <label for="form-radio-2">Sad</label>
        <input name="form-radio1" id="form-radio-2" value="Sad"
        type="radio" required=""></fieldset>
    </div>
    <div class="fieldcontain" id="fieldcontain-image-1">
        <div class="button-wrapper button-camera">
            <input name="form-image-1" id="form-image-1" type="file"
            accept="image/png" capture="camera" class="camera">
            <label for="form-image-1">Take</label>
        </div>
    </div>
    <div id="another_test_form-buttons" class="fieldcontain ui-grid-a">
    <div class="ui-block-a">
        <input type="submit" name="record" id="532_record" value="Save">
    </div>
    <div class="ui-block-b">
        <input type="button" name="cancel" id="532_cancel" value="Cancel">
    </div>
    </div>
</form>
```

#### for a record:

```bash
curl
localhost:8080/1.3/pcapi/records/dropbox/userid/record/record.json
```

Example output:

```JSON
{

"editor": "another test form.edtr",

"fields": [

{

"id": "fieldcontain-radio-1",

"label": "Choose",

"val": "Happy"

}

],

"name": "feelings",

"point": {

"lon": -3.179603088585148,

"lat": 55.940356699067394,

"alt": null

},

"timestamp": "2013-04-16T10:28:08.204Z"

}
```

### Create a record with POST

A POST request can point to either a file or a folder. The depth
of the path tree is important. If only the record name is
provided (depth is 1) then the POST data will be saved as
record.json inside that record folder. If that folder already
exists a new one will be created. This is best explained by
example:

Assuming the PATH is /myrecord (depth is 1):

If /myrecord does not exist then the file is saved at
/myrecord/record.json

If it does exist then the file is saved at /myrecord
(2)/record.json (or keeps trying new folder names until a free
name is found)

If the PATH is /myrecord/somefile (depth is 2) then POST will
create that file or a similarly named file if it already
exists.

For *Cordova* compatibility, the file contents may be sent using
as multipart/form-data inside a field named file like in the
following example:

```bash
curl --form file=@somerecord.json
localhost:8080/1.3/pcapi/record/dropbox/userid/myrecord/myrecord.json
```

Example Output:

```JSON`
{"msg": "File uploaded", "path": "/records/myrecord/myrecord
(2).json", "error": 0}
```

### Update (overwrite) a record with PUT

A PUT request must always point to a file (normally a record
file or an asset file). If that file exists it will be
overwritten:

```bash
curl -X PUT -T myrecord
localhost:8080/1.3/pcapi/record/dropbox/userid/myrecord/myrecord.json
```

The optional parameter autoexport=true will also export the
record to the database table corresponding to the editor/form
that generated that record.

Example Output:

```JSON
{"msg": "File uploaded", "path":
"/records/myrecord/myrecord.json", "error": 0}
```

### Upload an editor (aka survey)

Same call as geteditors but issued as a PUT request:

```bash
curl -X PUT -T myeditor
localhost:8080/1.3/pcapi/editor/dropbox/userid/myeditor
```

Example Output:

```JSON
{"msg": "File uploaded", "path": "/editors/hggjg.edtr", "error":
0}
```

### Delete record

This is an example of a DELETE request:

curl -X DELETE
localhost:8080/1.3/pcapi/records/dropbox/userid/record

The response we get is:

{"msg": "/records/record deleted", "error": 0}

### Publish record to PostGIS and (optionally) a Geoserver W*S endpoint

Publishes a record after it has been uploaded with all its
assets. Publication depends on a preconfigured PostGIS database
specified in pcapi.ini. Optionally a Geoserver endpoint can also
be configured to provide access to those records from an OGC
compliant WMS/WFS interface.

```bash
curl
localhost:8080/1.3/pcapi/records/local/userid/record?ogc_sync=true
```

The nominal response is:

```JSON
{"msg": "INSERT 1 0", "error": 0}
```

### Synchronize records

Synchronization is currently implemented using a simple
scheme — it answers the question "What has changed in the
remote filesystem since last time I asked?". It is implemented
as a single call with an optional CURSOR parameter:

`https://localhost:8080/1.3/pcapi/sync/PROVIDER/USERID`

or

`https://localhost:8080/1.3/pcapi/sync/PROVIDER/USERID/CURSOR`

Where:

`USERID`

The USERID returned from a valid authentication.

`PROVIDER`

The storage provider (e.g. Dropbox) which must return synchronize
in its capabilities.

`CURSOR (optional)`

A string of characters that represent the state of the
filesystem at some point in time. By omitting this argument a
new cursor string is created

Returns:

A JSON object with a list of deleted and updated files.

### Synchronization example:

First get a cursor string which represents the current state of
the filesystem

```bash
curl
https://localhost:8080/1.3/pcapi/sync/dropbox/tchzufdt438y76q
```

This will return a JSON object similar to:

```JSON
{"cursor":
"Au92d4xq943JlFRE9apZ_IN4VNL15fbjTY8UrtoZgSvAeJxjZcjYzcA4Y",
"error": 0}
```

The cursor string should be stored and reused every time a sync
is required. E.g. If 2 image files were added (or modified) and
another one was deleted the following API call will provide that
information:

```bash
curl
https://localhost:8080/1.3/pcapi/sync/dropbox/tchzufdt438y76q/Au92d4xq943JlFRE9apZ_IN4VNL15fbjTY8UrtoZgSvAeJxjZcjYzcA4Y
```

Which will return something like:

```JSON
{"deleted": ["/records/image1.jpg","/records/image2.jpg"],
"updated": ["/records/record2/audio.wav"], "error": 0}
```

The client app should then update its local cache by deleting
all entries under deleted and by downloading/overwriting all
entries under updated. After synching is complete the client
would normally request a new cursor string to reset the
tracking of the filesystem to its current state.

2.5. Authentication :

Authentication used to be based on oAuth but is now obsoleted in favour of
external authentication / authorization mechanisms.

Currently PCAPI can work with all sorts REST authentication mechanisms from the
 basic security to very complex SAML based federation.

The following rules have to be followed:

1. Use HTTPS everyone (disable HTTP altogether)
2. Apply any existing REST security mechanism to provide a unique user-specific security token as
USERID in: `https://localhost:8080/1.3/pcapi/(.*)/local/USERID/(.*)`
