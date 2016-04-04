"""Module to produce a WFS GetCapabilities reponse. The reponse includes all
available featurestypes
"""

import os, json

from pcapi import logtool, config
from bottle import template

log = logtool.getLogger("WFS", "pcapi.ows")


def _error(msg):
    log.error(msg)
    return {"error": 1, "msg": msg}


def dispatch(http_request, http_response):
    """Main function that dispatches the right function accrording to HTTP
    Request and response headers.
    """
    wfs_version = http_request.GET.get("VERSION")
    if not wfs_version:
        return _error("ERROR: WFS version was not specified!")
    if ((wfs_version != "1.1.0") and (wfs_version != "1.0.0")):
        return _error("WFS version %s is not supported" % wfs_version)

    wfs_request = http_request.GET.get("REQUEST")
    if wfs_request:
        wfs_request = wfs_request.upper()
        if (wfs_request == "GETCAPABILITIES"):
            return getcapabilities(http_request, http_response, wfs_version)
        else:
            return _error("Request %s is not supported" % wfs_request)
    else:
        return _error("Request is not defined")


def getcapabilities(http_request, http_response, wfs_version):
    """WFS GetCapalities interface
    @param http_request(HTTPRequest): request headers
    @param http_request(string): response headers
    @param wfs_version(string): the WFS version (e.g. 1.1.0)
    """
    res = {"error": 1, "msg": "WFS GetCapalities unsuccessful"}
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
                       WFS_FEATURES=FEATURES)
    if res:
        http_response.content_type = 'text/xml; charset=utf-8'
    return res

if __name__ == "__main__":
    import sys
    if (len(sys.argv) != 2):
        print """USAGE: python wfs_getcapabilities.py templatefile """
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
