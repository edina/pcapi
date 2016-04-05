"""Handles routes for OWS services. You can still test each service without HTTP
by invoking them e.g. python ./wfs.py
"""

from pcapi import logtool,config

import WFS

log = logtool.getLogger("OWS", "pcapi.ows")


def _error(msg):
    log.error(msg)
    return {"error":1, "msg":msg}


def OWSRest(request, response):
    """Handles HTTP calls and dispatches the right OWS function
    @param request(string):request headers
    @param response(string): response headers
    """
    if not config.getboolean("ows","enable"):
        return _error("OWS support is disabled")
    ows_service = request.GET.get("SERVICE")
    if ows_service:
        ows_service = ows_service.upper()
    if not (ows_service):
        return _error("No OWS SERVICE specified")

    if (ows_service == "WFS"):
        return WFS.dispatch(request,response)
    if (ows_service == "SOS"):
        return _error("SOS is still WIP. Try WFS!")
        # return sos.dispatch(request,response)
    else:
        return _error("Service %s is not supported" % ows_service)
