<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">

    <xsl:param name="translations" select="document('translations.xml')"/>

    <xsl:template name="translation">
        <xsl:param name="key"/>
        <xsl:param name="language"/>
        
        <xsl:copy-of select="$translations/translations/translate[@key = $key]/language[@key = $language]/text()"/>

    </xsl:template>

</xsl:stylesheet>