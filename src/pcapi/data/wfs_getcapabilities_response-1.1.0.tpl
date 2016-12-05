<?xml version="1.0" encoding="UTF-8"?>
<wfs:WFS_Capabilities xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.opengis.net/wfs" xmlns:wfs="http://www.opengis.net/wfs" xmlns:ows="http://www.opengis.net/ows" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:cobweb="cobweb" version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd">
  <ows:ServiceIdentification>
    <ows:Title/>
    <ows:Abstract/>
    <ows:ServiceType>WFS</ows:ServiceType>
    <ows:ServiceTypeVersion>1.1.0</ows:ServiceTypeVersion>
    <ows:Fees/>
    <ows:AccessConstraints/>
  </ows:ServiceIdentification>
  <ows:ServiceProvider>
    <ows:ProviderName/>
    <ows:ServiceContact>
      <ows:IndividualName/>
      <ows:PositionName/>
      <ows:ContactInfo>
        <ows:Phone>
          <ows:Voice/>
          <ows:Facsimile/>
        </ows:Phone>
        <ows:Address>
          <ows:City/>
          <ows:AdministrativeArea/>
          <ows:PostalCode/>
          <ows:Country/>
        </ows:Address>
      </ows:ContactInfo>
    </ows:ServiceContact>
  </ows:ServiceProvider>
  <ows:OperationsMetadata>
    <ows:Operation name="GetCapabilities">
      <ows:DCP>
        <ows:HTTP>
          <ows:Get xlink:href="{{OWS_ENDPOINT}}"/>
          <ows:Post xlink:href="{{OWS_ENDPOINT}}"/>
        </ows:HTTP>
      </ows:DCP>
      <ows:Parameter name="AcceptVersions">
        <ows:Value>1.0.0</ows:Value>
        <ows:Value>1.1.0</ows:Value>
      </ows:Parameter>
      <ows:Parameter name="AcceptFormats">
        <ows:Value>text/xml</ows:Value>
      </ows:Parameter>
    </ows:Operation>
    <ows:Operation name="DescribeFeatureType">
      <ows:DCP>
        <ows:HTTP>
          <ows:Get xlink:href="{{OWS_ENDPOINT}}"/>
          <ows:Post xlink:href="{{OWS_ENDPOINT}}"/>
        </ows:HTTP>
      </ows:DCP>
      <ows:Parameter name="outputFormat">
        <ows:Value>text/xml; subtype=gml/3.1.1</ows:Value>
      </ows:Parameter>
    </ows:Operation>
    <ows:Operation name="GetFeature">
      <ows:DCP>
        <ows:HTTP>
          <ows:Get xlink:href="{{OWS_ENDPOINT}}"/>
          <ows:Post xlink:href="{{OWS_ENDPOINT}}"/>
        </ows:HTTP>
      </ows:DCP>
      <ows:Parameter name="resultType">
        <ows:Value>results</ows:Value>
        <ows:Value>hits</ows:Value>
      </ows:Parameter>
      <ows:Parameter name="outputFormat">
        <ows:Value>GML2</ows:Value>
        <ows:Value>text/xml; subtype=gml/2.1.2</ows:Value>
        <ows:Value>text/xml; subtype=gml/3.1.1</ows:Value>
        <ows:Value>text/xml; subtype=gml/3.2</ows:Value>
        <ows:Value>application/json</ows:Value>
<!--
        <ows:Value>application/gml+xml; version=3.2</ows:Value>
        <ows:Value>application/vnd.google-earth.kml xml</ows:Value>
        <ows:Value>application/vnd.google-earth.kml+xml</ows:Value>
        <ows:Value>gml3</ows:Value>
        <ows:Value>gml32</ows:Value>
        <ows:Value>json</ows:Value>
-->
      </ows:Parameter>
      <ows:Constraint name="LocalTraverseXLinkScope">
        <ows:Value>2</ows:Value>
      </ows:Constraint>
    </ows:Operation>
    <ows:Operation name="GetGmlObject">
      <ows:DCP>
        <ows:HTTP>
          <ows:Get xlink:href="{{OWS_ENDPOINT}}"/>
          <ows:Post xlink:href="{{OWS_ENDPOINT}}"/>
        </ows:HTTP>
      </ows:DCP>
    </ows:Operation>
  </ows:OperationsMetadata>
  <FeatureTypeList>
    <Operations>
      <Operation>Query</Operation>
    </Operations>
    %for TYPENAME in WFS_FEATURES:
    <FeatureType xmlns:cobweb="cobweb">
      <Name>{{TYPENAME}}</Name>
      <Title>{{WFS_FEATURES[TYPENAME]["title"]}}</Title>
      <Abstract/>
      <ows:Keywords>
        <ows:Keyword>COBWEB SID</ows:Keyword>
        <ows:Keyword>{{WFS_FEATURES[TYPENAME]["sid"]}}</ows:Keyword>
      </ows:Keywords>
      <DefaultSRS>urn:x-ogc:def:crs:EPSG:4326</DefaultSRS>
      <ows:WGS84BoundingBox>
        <ows:LowerCorner>7.83788872494062 51.349933648803</ows:LowerCorner>
        <ows:UpperCorner>8.4850505833372 51.481028227907</ows:UpperCorner>
      </ows:WGS84BoundingBox>
    </FeatureType>
    %end
  </FeatureTypeList>
  <ogc:Filter_Capabilities>
    <ogc:Spatial_Capabilities>
      <ogc:GeometryOperands>
        <ogc:GeometryOperand>gml:Envelope</ogc:GeometryOperand>
      </ogc:GeometryOperands>
      <ogc:SpatialOperators>
        <ogc:SpatialOperator name="BBOX"/>
      </ogc:SpatialOperators>
    </ogc:Spatial_Capabilities>
    <ogc:Scalar_Capabilities>
      <ogc:LogicalOperators/>
      <ogc:ComparisonOperators>
        <ogc:ComparisonOperator>EqualTo</ogc:ComparisonOperator>
      </ogc:ComparisonOperators>
      <ogc:ArithmeticOperators>
        <ogc:SimpleArithmetic/>
        <ogc:Functions>
          <ogc:FunctionNames>
            <ogc:FunctionName nArgs="2">within</ogc:FunctionName>
          </ogc:FunctionNames>
        </ogc:Functions>
      </ogc:ArithmeticOperators>
    </ogc:Scalar_Capabilities>
    <ogc:Id_Capabilities>
      <ogc:FID/>
      <ogc:EID/>
    </ogc:Id_Capabilities>
  </ogc:Filter_Capabilities>
</wfs:WFS_Capabilities>
