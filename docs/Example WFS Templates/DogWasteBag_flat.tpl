% import urllib2
<?xml version="1.0" encoding="UTF-8"?>
<wfs:FeatureCollection xmlns="http://www.opengis.net/wfs" xmlns:wfs="http://www.opengis.net/wfs" xmlns:cobweb="cobweb" xmlns:gml="http://www.opengis.net/gml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="cobweb {{OWS_ENDPOINT}}?Service=WFS&amp;VERSION=1.0.0&amp;typeName=cobweb:HT_Protokoll_Flat&amp;REQUEST=DescribeFeatureType http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.0.0/WFS-basic.xsd">
  <gml:boundedBy>
    <gml:Box srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">
      <gml:coordinates xmlns:gml="http://www.opengis.net/gml" decimal="." cs="," ts=" ">23.9584,35.2913 23.9584,35.2913</gml:coordinates>
    </gml:Box>
  </gml:boundedBy>
  %for FEATURE in FC["features"]:
  % (lon,lat) = (FEATURE["geometry"]["coordinates"][0],FEATURE["geometry"]["coordinates"][1])
  <gml:featureMember>
    <cobweb:HT_Protokoll_Flat fid="{{FEATURE["properties"]["id"]}}">
      <gml:boundedBy>
        <gml:Box srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">
          <gml:coordinates xmlns:gml="http://www.opengis.net/gml" decimal="." cs="," ts=" ">{{lon}},{{lat}} {{lon}},{{lat}}</gml:coordinates>
        </gml:Box>
      </gml:boundedBy>
      <cobweb:Bemerkungen>{{[ x["val"] for x in FEATURE["properties"]["fields"] if x["id"] == "text-1" ][0]}}</cobweb:Bemerkungen>
      <cobweb:Zeitstempel>{{FEATURE["properties"]["timestamp"]}}</cobweb:Zeitstempel>
      <cobweb:Gefüllt>{{[ x["val"] for x in FEATURE["properties"]["fields"] if x["id"] == "radio-1" ][0]}}</cobweb:Gefüllt>
      % image = [ x["val"] for x in FEATURE["properties"]["fields"] if x["id"] == "image-1" ][0]
      % base_url = "https://IMAGE_ENDPOINT/" + urllib2.quote(FEATURE["name"].encode("utf-8"))
      <cobweb:Foto>{{base_url}}/{{image}}</cobweb:Foto>
      <cobweb:UserId>{{FEATURE["properties"]["original_uuid"]}}</cobweb:UserId>
      <cobweb:geom>
        <gml:Point srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">
          <gml:coordinates xmlns:gml="http://www.opengis.net/gml" decimal="." cs="," ts=" ">{{lon}},{{lat}}</gml:coordinates>
        </gml:Point>
      </cobweb:geom>
    </cobweb:HT_Protokoll_Flat>
  </gml:featureMember>
  %end
</wfs:FeatureCollection>
