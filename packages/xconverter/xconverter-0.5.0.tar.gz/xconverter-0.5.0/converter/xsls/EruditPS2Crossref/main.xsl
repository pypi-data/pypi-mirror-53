<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    xmlns="http://www.crossref.org/schema/4.4.1"
    xmlns:ai="http://www.crossref.org/AccessIndicators.xsd"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    xmlns:str="http://exslt.org/strings"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:converter="converter"
    exclude-result-prefixes="converter xs str" version="2.0">

    <xsl:variable name="document_language" select="article/@xml:lang"/>
    
    <xsl:template match="article">
        <doi_batch xsi:schemaLocation="http://www.crossref.org/schema/4.4.1 http://www.crossref.org/schemas/crossref4.4.1.xsd" version="4.4.1">
            <xsl:copy-of select="converter:head(.)"/>
            <body>
                <journal>
                    <journal_metadata>
                        <full_title>
                            <xsl:value-of select="front/journal-meta/journal-title-group/journal-title"/><xsl:if test="front/journal-meta/journal-title-group/journal-subtitle"><xsl:value-of select="concatenate(' : ',front/journal-meta/journal-title-group/journal-subtitle)"/></xsl:if>
                        </full_title>
                        <xsl:apply-templates select="front/journal-meta/journal-title-group/abbrev-journal-title"/>
                        <xsl:apply-templates select="front/journal-meta/issn"/>
                    </journal_metadata>
                    <journal_issue>
                        <xsl:apply-templates select="front/article-meta/article-categories/subj-group[@subj-group-type='heading']/subject" mode="issue-subtitle"/>
                        <xsl:apply-templates select="front/article-meta/pub-date[@date-type='collection']" mode="print"/>
                        <xsl:apply-templates select="front/article-meta/volume"/>
                        <xsl:apply-templates select="front/article-meta/issue"/>
                    </journal_issue>
                    <journal_article publication_type="full_text" reference_distribution_opts="any">
                        <xsl:attribute name="language"><xsl:value-of select="$document_language"/></xsl:attribute>
                        <titles>
                            <xsl:apply-templates select="front/article-meta/title-group/article-title[@xml:lang=$document_language]"/>
                            <xsl:apply-templates select="front/article-meta/product/related-object" mode="review-title"/>
                            <xsl:apply-templates select="front/article-meta/title-group/subtitle[@xml:lang=$document_language]"/>
                        </titles>
                        <xsl:if test="front/article-meta/contrib-group">
                            <contributors>
                                <xsl:apply-templates select="front/article-meta/contrib-group//contrib"/>
                            </contributors>
                        </xsl:if>
                        <xsl:apply-templates select="front/article-meta/abstract|front/article-meta/trans-abstract"/>
                        <xsl:apply-templates select="front/article-meta/pub-date[@date-type='pub']" mode="electronic"/>
                        <xsl:if test="front/article-meta/fpage|front/article-meta/fpage|front/article-meta/lpage|front/article-meta/elocation">
                            <pages>
                                <xsl:apply-templates select="front/article-meta/fpage|front/article-meta/fpage|front/article-meta/lpage|front/article-meta/elocation"/>
                            </pages>
                        </xsl:if>
                        <xsl:apply-templates select="front/article-meta/article-id[@pub-id-type='publisher-id']" mode="publisher-id"/>
                        <!--
                            Embargo must be included in Metadata API, it is not available in the EruditArticle XML file.
                        <xsl:apply-templates select="front/article-meta/permissions/license"/>
                        -->
                        <xsl:apply-templates select="front/article-meta/article-id[@pub-id-type='doi']" mode="doi"/>
                        <xsl:apply-templates select="back/ref-list"/>
                    </journal_article>
                </journal>
            </body>
        </doi_batch>
    </xsl:template>

    <xsl:template match="subject" mode="issue-subtitle">
        <titles>
            <xsl:value-of select="."/>
        </titles>
    </xsl:template>

    <xsl:template match="license">
        <ai:program name="AccessIndicators">
            <free_to_read/>
            <ai:license_ref applies_to="vor"><xsl:value-of select="@xlink:href"/></ai:license_ref>
            <ai:license_ref applies_to="tdm"><xsl:value-of select="@xlink:href"/></ai:license_ref>
        </ai:program>
    </xsl:template>

    <xsl:template match="ref-list">
        <citation_list>
            <xsl:apply-templates select="ref/element-citation/styled-content[@specific-use='display']|ref/mixed-citation" mode="references"/>
        </citation_list>
    </xsl:template>

    <xsl:template match="styled-content" mode="references">
        <citation>
            <xsl:attribute name="key">
                <xsl:value-of select="../../@id"/>
            </xsl:attribute>
            <xsl:apply-templates select="../pub-id[@pub-id-type='doi']" mode="doi"/>
            <unstructured_citation>
                <xsl:apply-templates select="*|text()"/>
            </unstructured_citation>
    </citation>
    </xsl:template>

    <xsl:template match="mixed-citation" mode="references">
        <citation>
            <xsl:attribute name="key">
                <xsl:value-of select="../@id"/>
            </xsl:attribute>
            <xsl:apply-templates select="../element-citation/pub-id[@pub-id-type='doi']" mode="doi"/>
            <unstructured_citation>
                <xsl:apply-templates select="*|text()"/>
            </unstructured_citation>
        </citation>
    </xsl:template>

    <xsl:template match="pub-id" mode="doi">
        <doi>
            <xsl:value-of select="."/>
        </doi>
    </xsl:template>

    <xsl:template match="article-id" mode="publisher-id">
        <publisher_item>
            <identifier id_type="pii"><xsl:value-of select="."/></identifier>
        </publisher_item>
    </xsl:template>

    <xsl:template match="article-id" mode="doi">
        <doi_data>
            <doi><xsl:value-of select="."/></doi>
            <resource>http://id.erudit.org/iderudit/<xsl:value-of select="../article-id[@pub-id-type='publisher-id']/text()"/></resource>
        </doi_data>
    </xsl:template>

    <xsl:template match="fpage">
        <first_page>
            <xsl:value-of select="."/>
        </first_page>
    </xsl:template>

    <xsl:template match="lpage">
        <xsl:if test="../fpage != .">
            <last_page>
                <xsl:value-of select="."/>
            </last_page>
        </xsl:if>
    </xsl:template>

    <xsl:template match="elocation">
        <other_pages>
            <xsl:value-of select="."/>
        </other_pages>
    </xsl:template>

    <xsl:template match="abbrev-journal-title">
        <abbrev_title><xsl:value-of select="."/></abbrev_title>
    </xsl:template>

    <xsl:template match="issn">
        <issn>
            <xsl:attribute name="media_type">
                <xsl:choose>
                    <xsl:when test="@pub-type='epub'">electronic</xsl:when>
                    <xsl:otherwise>print</xsl:otherwise>
                </xsl:choose>
            </xsl:attribute>
            <xsl:value-of select="."/>
        </issn>
    </xsl:template>

    <xsl:template match="pub-date" mode="print">
        <!-- Original Journal publication date "Issue Publication Date"-->
        <!-- Note that crossref do not support season in dates. When available -->
        <!-- in the input XML, it will be ignored to produce the Crossref XML. -->
        <publication_date media_type="print">
            <xsl:apply-templates select="month"/>
            <xsl:apply-templates select="day"/>
            <xsl:apply-templates select="year"/>
        </publication_date>
    </xsl:template>

    <xsl:template match="pub-date" mode="electronic">
        <!-- Electronic publication date in the platform Érudit-->
        <publication_date media_type="online">
            <xsl:apply-templates select="month"/>
            <xsl:apply-templates select="day"/>
            <xsl:apply-templates select="year"/>
        </publication_date>
    </xsl:template>

    <xsl:template match="day">
        <day>
            <xsl:value-of select="."/>
        </day>
    </xsl:template>

    <xsl:template match="month">
        <month>
            <xsl:value-of select="."/>
        </month>
    </xsl:template>

    <xsl:template match="year">
        <year>
            <xsl:value-of select="."/>
        </year>
    </xsl:template>

    <xsl:template match="volume">
        <journal_volume>
            <volume><xsl:value-of select="."/></volume>
        </journal_volume>
    </xsl:template>

    <xsl:template match="issue">
        <issue><xsl:value-of select="."/></issue>
    </xsl:template>

    <xsl:template match="article-title">
        <title>
            <xsl:value-of select="."/>
        </title>
    </xsl:template>

    <xsl:template match="subtitle">
        <subtitle>
            <xsl:value-of select="."/>
        </subtitle>
    </xsl:template>

    <xsl:template match="related-object" mode="review-title">
        <title>
            <xsl:value-of select="."/>
        </title>
    </xsl:template>

    <xsl:template match="contrib">
        <person_name>
            <xsl:attribute name="contributor_role">
                <xsl:value-of select="../@content-type"/>
            </xsl:attribute>
            <xsl:choose>
                <xsl:when test="count(preceding-sibling::contrib) + 1 = 1">
                    <xsl:attribute name="sequence">first</xsl:attribute>                    
                </xsl:when>
                <xsl:otherwise>
                    <xsl:attribute name="sequence">additional</xsl:attribute>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:apply-templates select="name/given-names"/>
            <xsl:apply-templates select="name/surname"/>
            <xsl:apply-templates select="name/suffix"/>
            <xsl:apply-templates select="xref[@ref-type='aff']" mode="aff"/>
            <xsl:apply-templates select="contrib-id[@contrib-id-type='orcid']" mode="orcid"/>
        </person_name>
    </xsl:template>

    <xsl:template match="xref" mode="aff">
        <xsl:variable name="rid" select="@rid"/>
        <xsl:apply-templates select="//aff[@id=$rid]"/>
    </xsl:template>

    <xsl:template match="aff">
        <affiliation>
            <xsl:value-of select="institution"/>
        </affiliation>
    </xsl:template>

    <xsl:template match="given-names">    
        <given_name><xsl:value-of select="."/></given_name>        
    </xsl:template>

    <xsl:template match="surname">
        <surname><xsl:value-of select="."/></surname>
    </xsl:template>

    <xsl:template match="suffix">
        <suffix><xsl:value-of select="substring(.,1,10)"/></suffix>
    </xsl:template>

    <xsl:template match="contrib-id" mode="orcid">
        <ORCID><xsl:value-of select="."/></ORCID>
    </xsl:template>

    <xsl:template match="abstract|trans-abstract">
        <jats:abstract>
            <xsl:attribute name="xml:lang">
                <xsl:choose>
                    <xsl:when test="@xml:lang=''">
                        <xsl:value-of select="$document_language"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="@xml:lang"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:attribute>
            <xsl:apply-templates select="*" mode="abstract-content"/>
        </jats:abstract>
    </xsl:template>

    <xsl:template match="*" mode="abstract-content">
        <xsl:variable name="elem_name"><xsl:if test="not(contains(':', name()))">jats:</xsl:if><xsl:value-of select="name()"/></xsl:variable>
        <xsl:element name="{$elem_name}">
            <xsl:apply-templates select="*|text()" mode="abstract-content"/>
        </xsl:element>
    </xsl:template>

</xsl:stylesheet>