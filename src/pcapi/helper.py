"""Just some static utility functions that can't be grouped anywhere else"""


def strfilter(text, remove):
    """
    remove chars defined in "remove" from "text"
    """
    return ''.join([c for c in text if c not in remove])


def basename(filename):
    r"""Converts uploaded filename from something like "C\foo\windows\name.zip
    to name
    """
    # remove suffix
    tmp = filename
    tmp = tmp[ :tmp.rfind('.')]
    # remove funny chars
    return strfilter(tmp, "\\/")


def httprequest2dict(http_request):
    """Convert bottle http request object into a case sensitive param dictionary
    as follows:
    1. Join POST and GET K/V pairs
    2. Lower case keys -- no point in case-sensitive GET/POST requests

    @param(http_request): a Bottle BaseHTTPRequest object
    @returns A dictionary with all values
    """

    join = {}
    for k in http_request.GET.dict:
        join[k.lower()] = http_request.GET.dict[k][0]
    for k in http_request.POST.dict:
        join[k.lower()] = http_request.POST.dict[k][0]
    return join
