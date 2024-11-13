<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" version="3.16.0-Hannover" labelsEnabled="0" simplifyDrawingHints="1" simplifyMaxScale="1" readOnly="0" minScale="100000000" styleCategories="AllStyleCategories" simplifyAlgorithm="0" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" simplifyDrawingTol="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal startField="" endExpression="" durationField="" mode="0" startExpression="" accumulate="0" fixedDuration="0" durationUnit="min" endField="" enabled="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 type="singleSymbol" forceraster="0" symbollevels="0" enableorderby="0">
    <symbols>
      <symbol type="fill" force_rhr="0" name="0" alpha="1" clip_to_extent="1">
        <layer locked="0" class="SimpleFill" pass="0" enabled="1">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="255,255,255,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="255,255,255,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.26" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" value="" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="fillColor">
                  <Option type="bool" value="true" name="active"/>
                  <Option type="QString" value="set_color_part(@value, 'alpha', (100-&quot;Xpar&quot;)*255/100)" name="expression"/>
                  <Option type="int" value="3" name="type"/>
                </Option>
                <Option type="Map" name="outlineColor">
                  <Option type="bool" value="true" name="active"/>
                  <Option type="QString" value="set_color_part(@value, 'alpha', (100-&quot;Xpar&quot;)*255/100)" name="expression"/>
                  <Option type="int" value="3" name="type"/>
                </Option>
              </Option>
              <Option type="QString" value="collection" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory height="15" enabled="0" labelPlacementMethod="XHeight" scaleDependency="Area" spacingUnitScale="3x:0,0,0,0,0,0" scaleBasedVisibility="0" penColor="#000000" direction="0" diagramOrientation="Up" lineSizeType="MM" backgroundColor="#ffffff" width="15" minScaleDenominator="0" spacing="5" lineSizeScale="3x:0,0,0,0,0,0" backgroundAlpha="255" maxScaleDenominator="1e+08" barWidth="5" opacity="1" sizeScale="3x:0,0,0,0,0,0" spacingUnit="MM" sizeType="MM" minimumSize="0" showAxis="1" penWidth="0" penAlpha="255" rotationOffset="270">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <axisSymbol>
        <symbol type="line" force_rhr="0" name="" alpha="1" clip_to_extent="1">
          <layer locked="0" class="SimpleLine" pass="0" enabled="1">
            <prop v="0" k="align_dash_pattern"/>
            <prop v="square" k="capstyle"/>
            <prop v="5;2" k="customdash"/>
            <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
            <prop v="MM" k="customdash_unit"/>
            <prop v="0" k="dash_pattern_offset"/>
            <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
            <prop v="MM" k="dash_pattern_offset_unit"/>
            <prop v="0" k="draw_inside_polygon"/>
            <prop v="bevel" k="joinstyle"/>
            <prop v="35,35,35,255" k="line_color"/>
            <prop v="solid" k="line_style"/>
            <prop v="0.26" k="line_width"/>
            <prop v="MM" k="line_width_unit"/>
            <prop v="0" k="offset"/>
            <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
            <prop v="MM" k="offset_unit"/>
            <prop v="0" k="ring_filter"/>
            <prop v="0" k="tweak_dash_pattern_on_corners"/>
            <prop v="0" k="use_custom_dash"/>
            <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" value="" name="name"/>
                <Option name="properties"/>
                <Option type="QString" value="collection" name="type"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings priority="0" linePlacementFlags="18" placement="1" zIndex="0" dist="0" showAll="1" obstacle="0">
    <properties>
      <Option type="Map">
        <Option type="QString" value="" name="name"/>
        <Option name="properties"/>
        <Option type="QString" value="collection" name="type"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration type="Map">
      <Option type="Map" name="QgsGeometryGapCheck">
        <Option type="double" value="0" name="allowedGapsBuffer"/>
        <Option type="bool" value="false" name="allowedGapsEnabled"/>
        <Option type="QString" value="" name="allowedGapsLayer"/>
      </Option>
    </checkConfiguration>
  </geometryOptions>
  <legend type="default-vector"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field name="FID_Conver" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Name" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="FID_Buffer" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Id" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="FromBufDst" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ToBufDist" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="xpar" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" name="" field="FID_Conver"/>
    <alias index="1" name="" field="Name"/>
    <alias index="2" name="" field="FID_Buffer"/>
    <alias index="3" name="" field="Id"/>
    <alias index="4" name="" field="FromBufDst"/>
    <alias index="5" name="" field="ToBufDist"/>
    <alias index="6" name="" field="xpar"/>
  </aliases>
  <defaults>
    <default expression="" field="FID_Conver" applyOnUpdate="0"/>
    <default expression="" field="Name" applyOnUpdate="0"/>
    <default expression="" field="FID_Buffer" applyOnUpdate="0"/>
    <default expression="" field="Id" applyOnUpdate="0"/>
    <default expression="" field="FromBufDst" applyOnUpdate="0"/>
    <default expression="" field="ToBufDist" applyOnUpdate="0"/>
    <default expression="" field="xpar" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" constraints="0" field="FID_Conver"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" constraints="0" field="Name"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" constraints="0" field="FID_Buffer"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" constraints="0" field="Id"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" constraints="0" field="FromBufDst"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" constraints="0" field="ToBufDist"/>
    <constraint notnull_strength="0" exp_strength="0" unique_strength="0" constraints="0" field="xpar"/>
  </constraints>
  <constraintExpressions>
    <constraint field="FID_Conver" exp="" desc=""/>
    <constraint field="Name" exp="" desc=""/>
    <constraint field="FID_Buffer" exp="" desc=""/>
    <constraint field="Id" exp="" desc=""/>
    <constraint field="FromBufDst" exp="" desc=""/>
    <constraint field="ToBufDist" exp="" desc=""/>
    <constraint field="xpar" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column type="field" width="-1" name="FID_Conver" hidden="0"/>
      <column type="field" width="-1" name="Name" hidden="0"/>
      <column type="field" width="-1" name="FID_Buffer" hidden="0"/>
      <column type="field" width="-1" name="Id" hidden="0"/>
      <column type="field" width="-1" name="FromBufDst" hidden="0"/>
      <column type="field" width="-1" name="ToBufDist" hidden="0"/>
      <column type="field" width="-1" name="xpar" hidden="0"/>
      <column type="actions" width="-1" hidden="1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field editable="1" name="FID_Buffer"/>
    <field editable="1" name="FID_Conver"/>
    <field editable="1" name="FromBufDst"/>
    <field editable="1" name="Id"/>
    <field editable="1" name="Name"/>
    <field editable="1" name="ToBufDist"/>
    <field editable="1" name="xpar"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="FID_Buffer"/>
    <field labelOnTop="0" name="FID_Conver"/>
    <field labelOnTop="0" name="FromBufDst"/>
    <field labelOnTop="0" name="Id"/>
    <field labelOnTop="0" name="Name"/>
    <field labelOnTop="0" name="ToBufDist"/>
    <field labelOnTop="0" name="xpar"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"Name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
