"""Module to produce a WFS GetCapabilities response. The response includes all
available featurestypes
"""

import os, json

from pcapi import logtool, config, helper, fs_provider
from pcapi.provider import Records
from bottle import template

log = logtool.getLogger("WFS", "pcapi.ows")


def _error(msg):
    log.error(msg)
    return {"error": 1, "msg": msg}


def dispatch(http_request, http_response):
    """Main function that dispatches the right function accrording to HTTP
    Request and response headers.
    """
    params = helper.httprequest2dict(http_request)

    wfs_version = params["version"] if "version" in params else None
    wfs_request = params["request"].upper() if "request" in params else None
    result = { "response":None, "mimetype":"application/json"}
    if not wfs_version:
        return _error("ERROR: WFS version was not specified!")
    if ((wfs_version != "1.1.0") and (wfs_version != "1.0.0")):
        return _error("WFS version %s is not supported" % wfs_version)
    if (wfs_request == "GETCAPABILITIES"):
        result = getcapabilities(params)
        if (result["error"] == 0):
            http_response.content_type = result["mimetype"]
        return result[ "response"]
    if (wfs_request == "DESCRIBEFEATURETYPE"):
        result = describefeaturetype(params)
        if (result["error"] == 0):
            http_response.content_type = result["mimetype"]
        return result[ "response"]
    if (wfs_request == "GETFEATURE"):
        result = getfeature(params)
        if (result["error"] == 0):
            http_response.content_type = result["mimetype"]
        return result[ "response"]
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
                                      "wfs_getcapabilities_response.tpl")

    with open(FEATURES_FILE) as f:
        FEATURES = json.load(f)

    with open(GETCAPABILITIES_FILE) as f:
        res = template(f.read(), OWS_ENDPOINT=ENDPOINT,
                       WFS_FEATURES=FEATURES, WFS_VERSION=params["version"])
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
        for k in FEATURES:
            if FEATURES[k]["name"] == TYPENAME:
                SID=k

    if not SID:
        return {"error": 1, "response": "featureType %s not found in features.json"
                % TYPENAME}

    XSD_FILE=os.path.join(config.get("path", "ows_template_dir"), SID + ".xsd")

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
    with open(FEATURES_FILE) as f:
        FEATURES = json.load(f)
        for k in FEATURES:
            if FEATURES[k]["name"] == TYPENAME:
                SID=k

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
                                    SID + ".tpl")
        if os.path.isfile(APPSCHEMA_FILE):
            with open(APPSCHEMA_FILE) as f:
                res = template(f.read(), FC=res, OWS_ENDPOINT=ENDPOINT,)
            return {"error": 0, "response": res, "mimetype":'text/xml; charset=utf-8'}
        else:
            return {"error": 1, "response": "Template not found for %s" % SID}
    else:
        return {"error": 1, "response": "WFS GetFeature unsuccessful"}

if __name__ == "__main__":
    import sys
    if (len(sys.argv) != 2):
        print """USAGE: python wfs.py templatefile """
        sys.exit(1)
    TPLFILE = sys.argv[1]

    # constants
    ENDPOINT='http://localhost:8080/pcapi/ows'
    FEATURES={"SID1": {"name": "cobweb:FeatureCollection1",
                       "title": "First Collection",
                       "template":"template1.tpl"},
              "SID2": {"name": "cobweb:FeatureCollection2",
                       "title": "Second Collection",
                       "template":"tempalte2.tpl"}}

    # print logs
    def dbg(x):
        print(x)
    log.debug = dbg

    res = template(open(TPLFILE).read(), OWS_ENDPOINT=ENDPOINT,
                   WFS_FEATURES=FEATURES)
    dbg(res)
    # validate:
    # xml = xml.dom.minidom.parseString(res)
    # dbg(xml.toprettyxml(indent='',newl=''))
