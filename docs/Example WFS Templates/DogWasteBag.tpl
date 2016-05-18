% import uuid
<?xml version="1.0" encoding="UTF-8"?>
<WasteBagObservationModel
  xmlns="http://cobwebproject.eu/GermanDemonstrator" xmlns:wfs="http://www.opengis.net/wfs/2.0" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink"
  xsi:schemaLocation="http://cobwebproject.eu/GermanDemonstrator GermanDemonstrator.xsd" gml:id="_1">
  <gml:boundedBy>
    <gml:Envelope srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">
      <gml:lowerCorner>7.83788872494062 51.349933648803</gml:lowerCorner>
      <gml:upperCorner>8.4850505833372 51.481028227907</gml:upperCorner>
    </gml:Envelope>
  </gml:boundedBy>
  %for FEATURE in FC["features"]:
  <observationMember>
    <WasteBag gml:id="{{FEATURE["properties"]["id"]}}">
      <Position gml:id="{{'_' + uuid.uuid4().get_hex()[:9]}}" srsName="EPSG:4326">
          <gml:pos>{{FEATURE["geometry"]["coordinates"][0]}} {{FEATURE["geometry"]["coordinates"][1]}}</gml:pos>
      </Position>
      <Zeitstempel>{{FEATURE["properties"]["timestamp"]}}</Zeitstempel>
      <Bemerkungen>{{[ x["val"] for x in FEATURE["properties"]["fields"] if x["id"] == "text-1" ][0]}}</Bemerkungen>
      <Gefüllt>{{[ x["val"] for x in FEATURE["properties"]["fields"] if x["id"] == "radio-1" ][0]}}</Gefüllt>
      % image = [ x["val"] for x in FEATURE["properties"]["fields"] if x["id"] == "image-1" ][0]
      % base_url = "https://IMAGE_ENDPOINT/" + FEATURE["name"]
      <Foto xlink:href="{{base_url}}/{{image}}"/>
      <UserId>{{FEATURE["properties"]["original_uuid"]}}</UserId>
    </WasteBag>
  </observationMember>
  %end
  <Erstellt>2016-03-23T17:53:00Z</Erstellt>
  <Zeitraum>
    <Begin>2016-01-28T15:34:27.546Z</Begin>
    <Ende>2016-01-28T22:21:22.044Z</Ende>
  </Zeitraum>
  <Survey xlink:href="https://de.cobweb.secure-dimensions.de/GermanDemonstratorSurvey.html"/>
</WasteBagObservationModel>
