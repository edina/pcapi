"""Module to produce a WFS GetCapabilities response. The response includes all
available featurestypes
"""

import os, json

from pcapi import logtool, config, fs_provider
from pcapi.provider import Records
from bottle import template

log = logtool.getLogger("WFS", "pcapi.ows")


def _error(msg):
    log.error(msg)
    return {"error": 1, "response": msg}


def dispatch(params, http_response):
    """Main function that dispatches the right function accrording to HTTP
    Request and response headers.
    @param params(dict): request headers
    """
    wfs_version = params["version"] if "version" in params else None
    wfs_request = params["request"].upper() if "request" in params else None
    if not wfs_version:
        return _error("ERROR: WFS version was not specified!")
    if ((wfs_version != "1.1.0") and (wfs_version != "1.0.0")):
        return _error("WFS version %s is not supported" % wfs_version)
    if (wfs_request == "GETCAPABILITIES"):
        return getcapabilities(params)
    if (wfs_request == "DESCRIBEFEATURETYPE"):
        return describefeaturetype(params)
    if (wfs_request == "GETFEATURE"):
        return getfeature(params)
    return _error("Request %s is not supported" % wfs_request)


def getcapabilities(params):
    """WFS GetCapalities interface
    @param params(dict): request headers
    @returns dictionary with { response, mimetype, error }
    """
    FEATURES = None

    # Check mandatory arguments
    ENDPOINT=config.get("ows", "endpoint")
    FEATURES_FILE=os.path.join(config.get("path", "ows_template_dir"), "features.json")
    GETCAPABILITIES_FILE=os.path.join(config.get("path", "ows_template_dir"),
                                      "wfs_getcapabilities_response-%s.tpl" % params["version"])

    with open(FEATURES_FILE) as f:
        FEATURES = json.load(f)

    with open(GETCAPABILITIES_FILE) as f:
        res = template(f.read(), OWS_ENDPOINT=ENDPOINT,
                       WFS_FEATURES=FEATURES)
    if res:
        return {"error": 0, "response": res, "mimetype":'text/xml; charset=utf-8'}
    else:
        return {"error": 1, "response": "WFS GetCapalities unsuccessful"}


def describefeaturetype(params):
    """WFS DescribeFeatureType interface
    @param params(dict): request headers
    @returns dictionary with { response, mimetype, error }
    """
    ## Mandatory parametres
    if "typename" not in params:
        return {"error": 1, "response": "Missing 'typeName'"}
    TYPENAME = params["typename"]
    FEATURES_FILE=os.path.join(config.get("path", "ows_template_dir"), "features.json")

    SID = None
    with open(FEATURES_FILE) as f:
        FEATURES = json.load(f)
        if TYPENAME in FEATURES:
            SID=FEATURES[TYPENAME]["sid"]
            TPL_FILE=FEATURES[TYPENAME]["template"]

    if not SID:
        return {"error": 1, "response": "TypeName %s not found in features.json"
                % TYPENAME}

    XSD_FILE=os.path.join(config.get("path", "ows_template_dir"), TPL_FILE + ".xsd")

    try:
        with open(XSD_FILE) as f:
            return {"error": 0, "response": f.read(), "mimetype":'text/xml; charset=utf-8'}
    except IOError:
        return _error("Cannot open file %s.xsd" % SID)


def getfeature(params):
    """WFS GetFeature interface
    @param params(dict): request headers
    @returns dictionary with { response, mimetype, error }
    """
    ## Mandatory parametres
    if "typename" not in params:
        return {"error": 1, "response": "Missing 'typeName'"}
    TYPENAME = params["typename"]
    ENDPOINT=config.get("ows", "endpoint")
    FEATURES_FILE=os.path.join(config.get("path", "ows_template_dir"), "features.json")

    ## Optional parametres
    OUTPUTFORMAT = params["outputformat"] if "outputformat" in params else "text/xml; subtype=gml/3.1.1"

    SID = None
    TPL_FILE = None
    with open(FEATURES_FILE) as f:
        FEATURES = json.load(f)
        if TYPENAME in FEATURES:
            SID=FEATURES[TYPENAME]["sid"]
            TPL_FILE=FEATURES[TYPENAME]["template"]

    if not SID:
        return {"error": 1, "response": "featureType %s not found in features.json"
                % TYPENAME}

    if "test" in params and params["test"] == "1":
        uid = config.get("test", "test_uid")
    else:
        uid = config.get("path", "public_uid")

    fp = fs_provider.FsProvider(uid)
    # Join all records
    all_records = Records.create_records_cache(fp, "/records")
    # Filter by survey id
    filtered_records = Records.filter_data(all_records, "editor", uid, {"id":SID})
    # export ot GeoJSON (as Python dictionary)
    res = Records.convertToGeoJSON(filtered_records)

    if res:
        if (OUTPUTFORMAT == "application/json") or (OUTPUTFORMAT == "json"):
            return {"error": 0, "response": res, "mimetype": "application/json"}
        # If not JSON assume XML and pipe through template
        APPSCHEMA_FILE=os.path.join(config.get("path", "ows_template_dir"),
                                    TPL_FILE)
        if os.path.isfile(APPSCHEMA_FILE):
            with open(APPSCHEMA_FILE) as f:
                res = template(f.read(), FC=res, OWS_ENDPOINT=ENDPOINT,)
            return {"error": 0, "response": res, "mimetype":'text/xml; charset=utf-8'}
        else:
            return {"error": 1, "response": "Template not found for %s" % SID}
    else:
        return {"error": 1, "response": "WFS GetFeature unsuccessful"}

if __name__ == "__main__":
    """Quickly test complex feature template without using the web app
    """
    import sys
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", type=argparse.FileType('r'), required=True,
                    help="path to input GeoJSON file")
    ap.add_argument("-t", "--template", type=argparse.FileType('r'), required=True,
                    help="path to template file")
    ap.add_argument("-d", "--debug", type=int, default=0,
                    help="debug 0|1")
    args = vars(ap.parse_args())

    TEMPLATE = args["template"].read()
    JSON = json.load(args["input"])
    ENDPOINT = "http://locahost:8080/pcapi/ows?"

    # print logs
    def dbg(x):
        if args["debug"]:
            print(x)
    log.debug = dbg

    res = template(TEMPLATE, FC=JSON, OWS_ENDPOINT=ENDPOINT,)
    print res

    # validate:
    if args["debug"]:
        import xml
        xml = xml.dom.minidom.parseString(res)
        dbg(xml.toprettyxml(indent='',newl=''))
