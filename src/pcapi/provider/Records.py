"""High level, HTTP-agnostic record access and processing"""

import re, json

from pcapi import logtool
from pcapi.provider import filter_utils

import time

log = logtool.getLogger("provider", "records")


class Record(object):
    """Class to store record bodies and metadata in memory for fast access"""

    def __init__(self, content, metadata):
        """Store content and metadata"""
        self.content = content  # as a parsed json (dict)
        self.metadata = metadata  # as a dbox_provider.Metadata object


def convertToGeoJSON(records):
    """
    Export all records to geojson and return result.
    """
    # python dicts should be automatically converted to geojson by bottle
    # self.response.headers['Content-Type'] = 'application/json'
    features = []
    for r in records:
        # log.debug(r.content)
        # get first -and only- value of dictionary because records are an array of
        # [ { <name> : <geojson feature> } ....]
        f = r.content.values()[0]
        features.append(f)

    geojson_dict = {"type": "FeatureCollection", "features": features}
    return geojson_dict


def create_records_cache(provider, path):
    """Creates an array of Records classed (s.a.) after parsing all records under `path'.
    Assumes a valid session
    """
    ret = []
    # If we are in `/' then get all records
    for d in provider.metadata(path).lsdirs():
        recpath = "{0}/record.json".format(d)
        log.debug("Parsing records -- requesting {0}".format(recpath))

        try:
            buf, meta = provider.get_file_and_metadata(recpath)
            rec = json.loads(buf.read())
            folder = re.split("/+", recpath)[2]
            record = Record({folder: rec}, meta)
            ret.append(record)
            buf.close()
        except Exception as e:
            log.exception("Exception: " + str(e))
    return ret

def filter_records(provider, filters, userid, params={}):
    """
    Filter records.

    @param provider(object): pcapi provider object
    @param filters(array): array of filter terms
    @param userid(string): pcapi user identifier
    @param params(dict): dictionary with lower-case GET/POST parameters
    @returns filtered output as geojson (or all features when filters==[])
    """

    records = create_records_cache(provider, "/records")
    if len(records) > 0:
        return filter_data(records, filters, userid, params)
    else:
        return []


def filter_data(records_cache, filters, userid, params={}):
    """Filter records (as returned from records_cache)
    @param params(dict): dictionary with lower-case GET/POST parameters
    @returns filtered output as geojson (or all features when filters==[])
    """
    log.debug("Found %d records" % len(records_cache))
    if len(filters) > 0:
        if "editor" in filters:
            log.debug("filter by editor")
            ## "editor" filter requires param "id"
            if "id" not in params:
                return {"msg": 'missing parameter "id"', "error":1}
            ID = params["id"]
            tmp_cache = []
            for x in records_cache:
                for r in x.content.itervalues():
                    if x.content is not None:
                        if(r["properties"]["editor"]==ID) or \
                          (r["properties"]["editor"]==ID + ".json") or \
                          (r["properties"]["editor"]==ID + ".edtr"):
                            tmp_cache.append(x)
            records_cache = tmp_cache
            # records_cache = [r for r in records_cache.itervalues() if r is not None and r.content["editor"].lower() == f_id]
            log.debug("found filter by editor")
        if "date" in filters:
            ## "date" filter requires at least a "start_date"
            if "start_date" not in params:
                return {"msg": 'missing parameter "start_date"', "error":1}
            start_date = params["start_date"]
            end_date = params["end_date"] if "end_date" in params else None
            log.debug("filter by dates %s %s" % (start_date, repr(end_date)))
            try:
                # parse the dates to unix epoch format. End time defaults to localtime )
                epoch_start = time.mktime(time.strptime(start_date,"%Y%m%d_%H:%M:%S"))
                epoch_end = time.mktime(time.strptime(end_date,"%Y%m%d_%H:%M:%S")
                                        if end_date else time.localtime())
                log.debug("transformed dates %s %s" % (epoch_start, epoch_end))
            except ValueError:
                return {"msg": "Bad date given. An example date would be 20120327_23:05:12", "error": 1}
            records_cache = [ r for r in records_cache if
                              r.metadata.mtime() >= epoch_start and r.metadata.mtime() <= epoch_end]
            log.debug(len(records_cache))
        if "envelope" in filters:
            if "bbox" not in params:
                return {"msg": 'missing parameter "bbox"', "error":1}
            bbox = params["bbox"]
            log.debug("filter by bbox %s" % bbox)
            try:
                (xmin, ymin, xmax, ymax) = map(float, bbox.split(","))
            except AttributeError:
                # (None).split() gives AttributeError
                return {"msg": 'Parameter "bbox" was not specified', "error":1}
            except ValueError:
                return {"msg":
                        "Wrong format. Use bbox=xmin,ymin,xmax,ymax e.g. bbox=-2.2342,33.55,-2.2290,33.56",
                        "error":1}
            # convert to numbers
            tmp_cache = []
            for x in records_cache:
                for r in x.content.itervalues():
                    log.debug(r["point"])
                    try:
                        lon = float(r["geometry"]["coordinates"][0])
                        lat = float(r["geometry"]["coordinates"][1])
                    except ValueError:
                        return {"msg": "Aborting due to error parsing lat/lon of record %s"
                                % r["name"], "error": 1}
                    if lon >= xmin and lon <= xmax and lat >= ymin and lat<=ymax:
                        tmp_cache.append(x)
            records_cache = tmp_cache
        if "pip" in filters:
            tmp_cache = []
            if "poly" in params:
                try:
                    poly = json.loads(params['poly'])
                    for record in records_cache:
                        geom = record.content.itervalues().next()['geometry']
                        if geom['type'] == 'Point':
                            coords = geom['coordinates']
                            if filter_utils.point_in_poly(coords[0], coords[1], poly):
                                tmp_cache.append(record)
                except ValueError as e:
                    # invalid json
                    return {"msg": e.message, "error":1}

            records_cache = tmp_cache
        if "format" in filters:
            if "frmt" not in params:
                return {"msg": 'missing parameter "frmt"', "error":1}
            frmt = params["frmt"]
            log.debug("filter by format %s" % frmt)
            if frmt == "geojson":
                return convertToGeoJSON(records_cache)
            else:
                return {"error":1, "msg": "unrecognised format: " + repr(frmt)}
    return records_cache
