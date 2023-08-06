<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:str="http://exslt.org/strings"
    xmlns:converter="converter"
    exclude-result-prefixes="converter xsi xs xlink mml str"
    version="2.0">

    <xsl:param name="reference_tab" select="document('reference_tab.xml')"/>
    <xsl:param name="restriction_tab" select="document('restriction_tab.xml')"/>
    
    <xsl:template name="reference_tab">
            <xsl:param name="group" />
            <xsl:param name="key" />
            <xsl:value-of select="$reference_tab/reference-tab/group[@value = $group]/key[@value = $key]"/>
    </xsl:template>

    <xsl:template name="restriction_tab">
        <xsl:param name="group" />
        <xsl:param name="key" />
        <xsl:value-of select="$reference_tab/reference-tab/group[@value = $group]/key[. = $key]"/>
    </xsl:template>
 
    <xsl:template match="@*" mode="attrif">
        <xsl:param name="attr_name" />
        <xsl:variable name="attr_value" select="."/>
        <xsl:if test="$attr_value != ''">
            <xsl:choose>
                <xsl:when test="$attr_name != ''">
                    <xsl:attribute name="{$attr_name}"><xsl:value-of select="$attr_value"/></xsl:attribute>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:attribute name="{name()}"><xsl:value-of select="$attr_value"/></xsl:attribute>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="*" mode="elemif">
        <xsl:param name="elem_name" />
        <xsl:variable name="elem_value" select="."/>
        <xsl:if test="$elem_value != ''">
            <xsl:choose>
                <xsl:when test="$elem_name != ''">
                    <xsl:element name="{$elem_name}">
                        <xsl:value-of select="$elem_value"/>
                    </xsl:element>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:element name="{name()}">
                        <xsl:value-of select="$elem_value"/>
                    </xsl:element>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
    </xsl:template>
 
</xsl:stylesheet>