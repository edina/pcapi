<?xml version="1.0" encoding="UTF-8"?>
<WFS_Capabilities xmlns="http://www.opengis.net/wfs" xmlns:cobweb="cobweb" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.0.0" xsi:schemaLocation="http://www.opengis.net/wfs https://dyfi.cobwebproject.eu:443/geoserver/schemas/wfs/1.0.0/WFS-capabilities.xsd">
  <Service>
    <Name>WFS</Name>
    <Title/>
    <Abstract/>
    <Keywords/>
    <OnlineResource>{{OWS_ENDPOINT}}</OnlineResource>
    <Fees/>
    <AccessConstraints/>
  </Service>
  <Capability>
    <Request>
      <GetCapabilities>
        <DCPType>
          <HTTP>
            <Get onlineResource="{{OWS_ENDPOINT}}?Service=WFS&amp;Version=1.0.0&amp;request=GetCapabilities"/>
          </HTTP>
        </DCPType>
        <DCPType>
          <HTTP>
            <Post onlineResource="{{OWS_ENDPOINT}}"/>
          </HTTP>
        </DCPType>
      </GetCapabilities>
      <DescribeFeatureType>
        <SchemaDescriptionLanguage>
          <XMLSCHEMA/>
        </SchemaDescriptionLanguage>
        <DCPType>
          <HTTP>
            <Get onlineResource="{{OWS_ENDPOINT}}?Service=WFS&amp;Version=1.0.0&amp;request=DescribeFeatureType"/>
          </HTTP>
        </DCPType>
        <DCPType>
          <HTTP>
            <Post onlineResource="{{OWS_ENDPOINT}}"/>
          </HTTP>
        </DCPType>
      </DescribeFeatureType>
      <GetFeature>
        <ResultFormat>
          <KML/>
          <GML2/>
          <GML3/>
          <SHAPE-ZIP/>
          <CSV/>
          <JSON/>
        </ResultFormat>
        <DCPType>
          <HTTP>
            <Get onlineResource="{{OWS_ENDPOINT}}?Service=WFS&amp;Version=1.0.0&amp;request=GetFeature"/>
          </HTTP>
        </DCPType>
        <DCPType>
          <HTTP>
            <Post onlineResource="{{OWS_ENDPOINT}}"/>
          </HTTP>
        </DCPType>
      </GetFeature>
    </Request>
  </Capability>
  <FeatureTypeList>
    <Operations>
      <Query/>
    </Operations>
    %for TYPENAME in WFS_FEATURES:
    <FeatureType>
      <Name>{{TYPENAME}}</Name>
      <Title>{{WFS_FEATURES[TYPENAME]["title"]}}</Title>
      <Abstract/>
      <Keywords>COBWEB, {{WFS_FEATURES[TYPENAME]["sid"]}}</Keywords>
      <SRS>EPSG:4326</SRS>
      <LatLongBoundingBox minx="7.83788872494062" miny="51.349933648803" maxx="8.4850505833372" maxy="51.481028227907"/>
    </FeatureType>
    %end
  </FeatureTypeList>
  <ogc:Filter_Capabilities>
    <ogc:Spatial_Capabilities>
      <ogc:Spatial_Operators>
        <ogc:BBOX/>
      </ogc:Spatial_Operators>
    </ogc:Spatial_Capabilities>
    <ogc:Scalar_Capabilities>
      <ogc:Logical_Operators/>
      <ogc:Comparison_Operators>
        <ogc:Simple_Comparisons/>
        <ogc:Between/>
        <ogc:Like/>
        <ogc:NullCheck/>
      </ogc:Comparison_Operators>
      <ogc:Arithmetic_Operators>
        <ogc:Simple_Arithmetic/>
        <ogc:Functions>
          <ogc:Function_Names>
            <ogc:Function_Name nArgs="2">within</ogc:Function_Name>
          </ogc:Function_Names>
        </ogc:Functions>
      </ogc:Arithmetic_Operators>
    </ogc:Scalar_Capabilities>
  </ogc:Filter_Capabilities>
</WFS_Capabilities>
