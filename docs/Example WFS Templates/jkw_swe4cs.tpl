% import uuid
% i = 0
<?xml version="1.0" encoding="UTF-8"?>
<cs:CitizenScienceObservationCollection xmlns:xlink="http://www.w3.org/1999/xlink"
 xmlns:gco="http://www.isotc211.org/2005/gco"
 xmlns:gmd="http://www.isotc211.org/2005/gmd"
 xmlns:gml="http://www.opengis.net/gml/3.2"
 xmlns:swe="http://www.opengis.net/swe/2.0"
 xmlns:sml="http://www.opengis.net/sensorml/2.0"
 xmlns:gss="http://www.isotc211.org/2005/gss"
 xmlns:cs="http://www.opengis.org/citizenscience/1.1"
 xmlns:om="http://www.opengis.net/om/2.0"
 xmlns:sams="http://www.opengis.net/samplingSpatial/2.0"
 xmlns:sf="http://www.opengis.net/sampling/2.0"
 xmlns:gts="http://www.isotc211.org/2005/gts"
 xmlns:gsr="http://www.isotc211.org/2005/gsr"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://www.opengis.org/citizenscience/1.1 file:/Users/isi/Dropbox/_workspace/ShapeChange-2.0.1/CitizenScience/output/xsd/INPUT/citizenScience.xsd" gml:id="ID000">
    <!-- Survey-wide Metadata come from the Portal in theory but from Survey Designer or manually in practice -->
    <cs:resultTime>
       <gml:TimeInstant gml:id="day1">
          <gml:timePosition>2015-06-12</gml:timePosition>
       </gml:TimeInstant>
    </cs:resultTime>
    <cs:metadata>
       <cs:CitizenScienceMetadata gml:id="m001">
          <cs:samplingCampaign>https://dyfi.cobwebproject.eu/URI/samplingCampaigns/JapKnotCampaign03</cs:samplingCampaign>
       </cs:CitizenScienceMetadata>
    </cs:metadata>
   <cs:procedure>
      <cs:CampaignProcess gml:id="cp001">
         <cs:samplingProtocol>https://dyfi.cobwebproject.eu/URI/samplingCampaigns/JapKnotCampaign03</cs:samplingProtocol>
         <cs:member>
            <cs:CitizenProcess gml:id="WG_Survey">
               <cs:recordedBy>
                  <cs:CitizenScientist gml:id="citzizen_ingo_25d9-f34e">
                     <cs:givenName>Name</cs:givenName>
                     <cs:lastName>Surname</cs:lastName>
                     <cs:email>email@mydomain.com</cs:email>
                     <cs:organization>My Organization</cs:organization>
                  </cs:CitizenScientist>
               </cs:recordedBy>
            </cs:CitizenProcess>
         </cs:member>
      </cs:CampaignProcess>
   </cs:procedure>
   <cs:observedProperty xlink:href="http://www.opengeospatial.org/skos/swe#fallopia_japonica" />
   <cs:result>
      <swe:DataArray>
         <swe:elementCount>
            <swe:Count>
               <swe:value>1</swe:value>
            </swe:Count>
         </swe:elementCount>
         <swe:elementType name="resultRecordStructure">
            <swe:DataRecord id="resultStructure">
               <swe:field name="plantHeight">
                  <swe:Text definition="https://dyfi.cobwebproject.eu/skos#plantHeight"/>
               </swe:field>
               <swe:field name="evidenceOfManagement">
                  <swe:Text definition="https://dyfi.cobwebproject.eu/skos#evidenceOfManagement"/>
               </swe:field>
               <swe:field name="distanceFromObservation">
                  <swe:Text definition="https://dyfi.cobwebproject.eu/skos#distanceFromObservation"/>
               </swe:field>
               <swe:field name="riverBankErrosion">
                  <swe:Text definition="https://dyfi.cobwebproject.eu/skos#riverBankErrosion"/>
               </swe:field>
               <swe:field name="broadHabitatType">
                  <swe:Text definition="https://dyfi.cobwebproject.eu/skos#BroadHabitatType"/>
               </swe:field>
               <swe:field name="temperature">
                  <swe:Text definition="https://dyfi.cobwebproject.eu/skos#Temperature"/>
               </swe:field>
               <swe:field name="weather">
                  <swe:Text definition="https://dyfi.cobwebproject.eu/skos#Weather"/>
               </swe:field>
               <swe:field name="photo">
                  <swe:Text definition="https://dyfi.cobwebproject.eu/skos#Photo"/>
               </swe:field>
               <swe:field name="positionAccuracy">
                  <swe:Count definition="https://dyfi.cobwebproject.eu/skos#positionAccuracy" />
               </swe:field>
            </swe:DataRecord>
         </swe:elementType>
         <swe:encoding>
            <swe:TextEncoding tokenSeparator="@@" blockSeparator="&#32;" decimalSeparator="."/>
         </swe:encoding>
      </swe:DataArray>
   </cs:result>
   <cs:featureOfInterest xlink:href="http://www.opengeospatial.org/features/Kriftel"/>
  %for FEATURE in FC["features"]:
   % i=i+1
   <cs:member>
      <cs:CitizenScienceObservation gml:id="{{FEATURE["properties"]["id"]}}">
          <om:phenomenonTime>
             <gml:TimeInstant gml:id="t{{str(i).zfill(4)}}">
                <gml:timePosition>{{FEATURE["properties"]["timestamp"]}}</gml:timePosition>
             </gml:TimeInstant>
          </om:phenomenonTime>
          <om:resultTime xlink:href="#t{{str(i).zfill(4)}}" />
          <om:procedure/>
          <om:observedProperty/>
          <om:featureOfInterest>
             <sams:SF_SpatialSamplingFeature gml:id="sf{{str(i).zfill(4)}}">
                <sf:type xlink:href="http://www.opengis.net/def/samplingFeatureType/OGC-OM/2.0/SF_SamplingPoint"/>
                <sf:sampledFeature xlink:href="http://www.opengeospatial.org/features/Kriftel"/>
                <sams:shape>
                   <gml:Point gml:id="sp{{i}}">
                      <gml:pos srsName="urn:ogc:def:crs:EPSG:4326">{{FEATURE["geometry"]["coordinates"][0]}} {{FEATURE["geometry"]["coordinates"][1]}}</gml:pos>
                   </gml:Point>
                </sams:shape>
            </sams:SF_SpatialSamplingFeature>
          </om:featureOfInterest>
          <om:result>
             <swe:DataRecord>
                %for prop in FEATURE["properties"]["fields"]:
                    %if (prop["id"] == "radio-2"):
                    <swe:field name="plantHeight">
                       <swe:Text definition="https://dyfi.cobwebproject.eu/skos#plantHeight">
                          <swe:value>{{prop["val"] if "val" in prop else "N/A"}}</swe:value>
                       </swe:Text>
                    </swe:field>
                    %end
                    %if (prop["id"] == "radio-3"):
                    <swe:field name="evidenceOfManagement">
                       <swe:Text definition="https://dyfi.cobwebproject.eu/skos#evidenceOfManagement">
                           <swe:value>{{prop["val"] if "val" in prop else "N/A"}}</swe:value>
                       </swe:Text>
                    </swe:field>
                    %end
                    %if (prop["id"] == "radio-7"):
                    <swe:field name="distanceFromObservation">
                       <swe:Text definition="https://dyfi.cobwebproject.eu/skos#distanceFromObservation">
                            <swe:value>{{prop["val"] if "val" in prop else "N/A"}}</swe:value>
                       </swe:Text>
                    </swe:field>
                    %end
                    %if (prop["id"] == "radio-4"):
                    <swe:field name="riverBankErrosion">
                       <swe:Text definition="https://dyfi.cobwebproject.eu/skos#riverBankErrosion">
                            <swe:value>{{prop["val"] if "val" in prop else "N/A"}}</swe:value>
                       </swe:Text>
                    </swe:field>
                    %end
                    %if (prop["id"] == "select-2"):
                    <swe:field name="broadHabitatType">
                       <swe:Text definition="https://dyfi.cobwebproject.eu/skos#BroadHabitatType">
                            <swe:value>{{prop["val"] if "val" in prop else "N/A"}}</swe:value>
                       </swe:Text>
                    </swe:field>
                    %end
                    %if (prop["id"] == "radio-6"):
                    <swe:field name="temperature">
                       <swe:Text definition="https://dyfi.cobwebproject.eu/skos#Temperature">
                            <swe:value>{{prop["val"] if "val" in prop else "N/A"}}</swe:value>
                       </swe:Text>
                    </swe:field>
                    %end
                    %if (prop["id"] == "radio-5"):
                    <swe:field name="weather">
                       <swe:Text definition="https://dyfi.cobwebproject.eu/skos#Weather">
                            <swe:value>{{prop["val"] if "val" in prop else "N/A"}}</swe:value>
                       </swe:Text>
                    </swe:field>
                    %end
                    %if (prop["id"] == "image-1"):
                    <swe:field name="photo">
                       <swe:Text definition="https://dyfi.cobwebproject.eu/skos#Photo">
                            <swe:value>{{prop["val"] if "val" in prop else "N/A"}}</swe:value>
                       </swe:Text>
                    </swe:field>
                    %end
                %end
                %if "pos_acc" in FEATURE["properties"]:
                <swe:field name="positionAccuracy">
                   <swe:Count definition="https://dyfi.cobwebproject.eu/skos#positionAccuracy">
                      <swe:value>{{FEATURE["properties"]["pos_acc"]}}</swe:value>
                   </swe:Count>
                </swe:field>
                %end
             </swe:DataRecord>
          </om:result>
       </cs:CitizenScienceObservation>
    </cs:member>
    %end
</cs:CitizenScienceObservationCollection>
