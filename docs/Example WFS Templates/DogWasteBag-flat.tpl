<?xml version="1.0" encoding="UTF-8"?>
<wfs:FeatureCollection xmlns="http://www.opengis.net/wfs" xmlns:wfs="http://www.opengis.net/wfs" xmlns:cobweb="cobweb" xmlns:gml="http://www.opengis.net/gml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="cobweb {{OWS_ENDPOINT}}?Service=WFS&amp;VERSION=1.0.0&amp;typeName=cobweb:HT_Protokoll&amp;REQUEST=DescribeFeatureType http://www.opengis.net/wfs schemas.opengis.net/wfs/1.0.0/WFS-basic.xsd">
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
      <cobweb:Notiz>{{[ x["val"] for x in FEATURE["properties"]["fields"] if x["id"] == "textarea-1" ][0]}}</cobweb:Notiz>
      <cobweb:Zeitstempel>{{FEATURE["properties"]["timestamp"]}}</cobweb:Zeitstempel>
      <cobweb:Foto>{{OWS_ENDPOINT}}/modified_1454019529641.jpg</cobweb:Foto>
      <cobweb:geom>
        <gml:Point srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">
          <gml:coordinates xmlns:gml="http://www.opengis.net/gml" decimal="." cs="," ts=" ">{{lon}},{{lat}}</gml:coordinates>
        </gml:Point>
      </cobweb:geom>
    </cobweb:HT_Protokoll_Flat>
  </gml:featureMember>
  %end
</wfs:FeatureCollection>
