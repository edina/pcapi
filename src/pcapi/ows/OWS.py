"""Handles routes for OWS services. You can still test each service without HTTP
by invoking them e.g. python ./wfs.py
"""

from pcapi import logtool,config, helper

import WFS

log = logtool.getLogger("OWS", "pcapi.ows")


def xmlerror(msg,http_response):
    log.error(msg)
    http_response.content_type = 'text/xml; charset=utf-8'
    ogc_error = """<ServiceExceptionReport xmlns="http://www.opengis.net/ogc" \
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2.0" \
    xsi:schemaLocation="http://www.opengis.net/ogc \
    http://schemas.opengis.net/wfs/1.0.0/OGC-exception.xsd">
        <ServiceException code="InvalidParameterValue" locator="typeName">{}</ServiceException>
    </ServiceExceptionReport>""".format(msg)
    return ogc_error


def OWSRest(http_request, http_response):
    """Handles HTTP calls and dispatches the right OWS function
    @param request(string):request headers
    @param response(string): response headers
    """
    if not config.getboolean("ows","enable"):
        return xmlerror("OWS support is disabled",http_response)
    params = helper.httprequest2dict(http_request)
    ows_service = params["service"].upper() if "service" in params else None
    if not (ows_service):
        return xmlerror("No OWS SERVICE specified",http_response)

    if (ows_service == "WFS"):
        result = WFS.dispatch(params,http_response)
        if (result["error"] == 0):
            http_response.content_type = result["mimetype"]
            return result[ "response"]
        return xmlerror(result["response"],http_response)

    if (ows_service == "SOS"):
        return xmlerror("SOS is still WIP. Try WFS!",http_response)
        # return sos.dispatch(request,response)
    else:
        return xmlerror("Service %s is not supported" % ows_service,http_response)
