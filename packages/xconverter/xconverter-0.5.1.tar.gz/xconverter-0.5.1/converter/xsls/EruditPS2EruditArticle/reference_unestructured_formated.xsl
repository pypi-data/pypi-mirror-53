<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    xmlns="http://www.erudit.org/xsd/article"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    xmlns:str="http://exslt.org/strings"
    xmlns:converter="converter"
    exclude-result-prefixes="converter xs xsi str mml xlink"
    version="2.0">
    
    <xsl:param name="reference_format"/>
    
    <xsl:template match="ref" mode="unestructured_formated"><refbiblio><xsl:if test="@id"><xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute></xsl:if><xsl:apply-templates select="element-citation/*" mode="unestructured_formated_elements"></xsl:apply-templates></refbiblio></xsl:template>
    
    <xsl:template match="*" mode="unestructured_formated_elements"><xsl:apply-templates select="*" mode="unestructured_formated_elements"/></xsl:template>
    
    <xsl:template match="*" mode="unestructured_formated_elements"><xsl:value-of select="."/>.</xsl:template>
    
    <xsl:template match="person-group" mode="unestructured_formated_elements"><xsl:value-of select="name/given-names"/>, <xsl:value-of select="name/surname"/>; </xsl:template>
    
    <xsl:template match="year" mode="unestructured_formated_elements">(<xsl:value-of select="."/>). </xsl:template>
    
    <xsl:template match="source" mode="unestructured_formated_elements"><marquage typemarq="italique"><xsl:value-of select="."/></marquage>, </xsl:template>
    
    <xsl:template match="article-title" mode="unestructured_formated_elements"><xsl:value-of select="."/>. </xsl:template>
    
    <xsl:template match="volume" mode="unestructured_formated_elements"><xsl:choose><xsl:when test="../issue != ''"><xsl:value-of select="."/>(<xsl:value-of select="../issue"/>), </xsl:when><xsl:otherwise><xsl:value-of select="." />, </xsl:otherwise></xsl:choose></xsl:template>
    
    <xsl:template match="issue" mode="unestructured_formated_elements"><xsl:if test="../volume = ''">(<xsl:value-of select="."/>), </xsl:if></xsl:template>
    
    <xsl:template match="fpage" mode="unestructured_formated_elements"><xsl:choose><xsl:when test="../lpage != ''">(<xsl:value-of select="."/>-<xsl:value-of select="../lpage"/>). </xsl:when><xsl:otherwise>(<xsl:value-of select="." />). </xsl:otherwise></xsl:choose></xsl:template>
    
    <xsl:template match="lpage" mode="unestructured_formated_elements"><xsl:if test="../lpage = ''">(<xsl:value-of select="."/>).</xsl:if></xsl:template>
    
    <xsl:template match="pub-id[@pub-id-type='doi']" mode="unestructured_formated_elements">DOI: http://doi.org/<xsl:value-of select="."/>/</xsl:template>
</xsl:stylesheet>