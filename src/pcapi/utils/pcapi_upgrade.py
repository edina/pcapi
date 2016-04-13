# -*- coding: utf-8 -*-
"""
Utility to convert all records from *.json to geojson *.json.

Algorithm:
    - Search all *.json files under data/records
    - if there are in the new format ignore them
    - else convert them and replace the old file
"""

import os,json

from pcapi import config, logtool

def find_json(dirname):
    """ Find all json files under dirname and return as list """
    for root, dirs, files in os.walk(dirname):
        for f in files:
            if f.endswith(".json"):
                yield os.path.join(root,f)

def rec2geojson(record):
    """ converts COBWEB records from json to geojson feature format

        Args:
            record (dict): dictionary representing parsed JSON record

        Returns:
            Dictionary representing GeoJSON record or None if it is already in
            the new format.
    """
    if (record.has_key('geometry') or not record.has_key('name')):
        return None
    geometry = {}
    geometry["type"] = "Point"
    geometry["coordinates"] = [record["point"]["lon"], record["point"]["lat"]]
    res = {}
    res["type"] = "Feature"
    res["geometry"] = geometry
    res["properties"] = record
    return res

def updateEditorExtension(record):
    """
    updates the editor to be from .edtr to .json
    """
    if record["properties"]["editor"].endswith(".edtr"):
        record["properties"]["editor"] = record["properties"]["editor"].replace(".edtr", ".json")
        return record
    return None

def updateIdInGeojson(record):
    """
    updates id of each field of the geojson to follow the updated format
    """
    if not record.has_key('geometry'):
        return None
    for i in range(len(record["properties"]["fields"])):
        field = record["properties"]["fields"][i]
        if "fieldcontain-" in field["id"]:
            record["properties"]["fields"][i]["id"] = field["id"].replace("fieldcontain-", "")
        else:
            return None
    return record

def upgrade_all_data():
    # normally ~/.pcapi/data
    data_dir = config.get("path","data_dir")
    for f in find_json(data_dir):
        j = json.load(open(f))
        gj = rec2geojson(j)
        if not gj:
            print "Ignoring %s which is already converted." % f
        else:
            print "Overwriting new version of %s" % f
            with open(f,'w') as fp:
                json.dump(gj,fp)
        new_gj = updateIdInGeojson(j)
        if not new_gj:
            print "Ignoring %s which is already converted." % f
        else:
            print "Overwriting new version of %s" % f
            with open(f,'w') as fp:
                json.dump(new_gj,fp)
        gj_new_ed_ext = updateEditorExtension(new_gj)
        if not gj_new_ed_ext:
            print "Ignoring %s which is already converted." % f
        else:
            print "Overwriting new version of %s" % f
            with open(f,'w') as fp:
                json.dump(gj_new_ed_ext,fp)

if __name__ == "__main__":
    upgrade_all_data()
