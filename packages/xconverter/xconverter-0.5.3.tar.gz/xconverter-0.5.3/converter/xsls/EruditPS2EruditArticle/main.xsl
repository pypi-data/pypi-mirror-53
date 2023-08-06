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
    
    <xsl:import href="utils.xsl"/>
    <xsl:import href="reference_unestructured_formated.xsl"/>
    <xsl:param name="reference_format"/>
    <xsl:output method="xml" encoding="utf-8" omit-xml-declaration="yes" indent="yes"/>

    <xsl:variable name="document_language" select="./article/@xml:lang"/>
 
    <xsl:template match="article">
        <article>
            <xsl:apply-templates select="@article-type" mode="attrif">
                <xsl:with-param name="attr_name">typeart</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="@xml:lang" mode="attrif">
                <xsl:with-param name="attr_name">lang</xsl:with-param>
            </xsl:apply-templates>
            <xsl:choose>
                <xsl:when test="boolean(front/article-meta/issue/@seq)">
                    <xsl:attribute name="ordseq"><xsl:value-of select="front/article-meta/issue/@seq"/></xsl:attribute>
                </xsl:when>
                <xsl:when test="boolean(front/article-meta/volume/@seq)">
                    <xsl:attribute name="ordseq"><xsl:value-of select="front/article-meta/volume/@seq"/></xsl:attribute>
                </xsl:when>
            </xsl:choose>
            <xsl:if test="front/article-meta/article-id[@pub-id-type='publisher-id']">
                <xsl:attribute name="idproprio"><xsl:value-of select="front/article-meta/article-id[@pub-id-type='publisher-id']"/></xsl:attribute>
            </xsl:if>        
            <xsl:apply-templates select="front"/>
            <xsl:apply-templates select="body"/>
            <xsl:apply-templates select="back"/>
        </article>
    </xsl:template>

    <xsl:template match="back">
        <partiesann>
            <xsl:attribute name="lang"><xsl:value-of select="$document_language"/></xsl:attribute>
            <xsl:apply-templates select="ack"/>
            <xsl:apply-templates select="ref-list"/>
            <xsl:if test="//bio">
                <grnotebio>
                    <xsl:apply-templates select="//bio"/>
                </grnotebio>
            </xsl:if>
        </partiesann>
    </xsl:template>

    <xsl:template match="ack">
        <merci>
            <xsl:apply-templates select="title"/>
            <xsl:apply-templates select="p"/>
        </merci>
    </xsl:template>

    <xsl:template match="ref-list">
        <grbiblio>
            <biblio>
                <xsl:choose>
                    <xsl:when test="$reference_format = 'unestructured_formated'">
                        <xsl:apply-templates select="ref" mode="unestructured_formated"/>
                    </xsl:when>
                    <xsl:when test="$reference_format = 'unestructured_unformated'">
                        <xsl:apply-templates select="ref" mode="unestructured_unformated"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:apply-templates select="ref" mode="unestructured_formated"/>
                    </xsl:otherwise>
                </xsl:choose>
            </biblio>
        </grbiblio>
    </xsl:template>

    <xsl:template match="bio">
        <notebio>
            <xsl:attribute name="id">
                <xsl:value-of select="@id"/>
            </xsl:attribute>
            <xsl:attribute name="idrefs">
                <xsl:value-of select="../@id"/>
            </xsl:attribute>
            <xsl:attribute name="lang">
                <xsl:choose>
                    <xsl:when test="@xml:lang"><xsl:value-of select="@xml:lang"/></xsl:when>
                    <xsl:otherwise><xsl:value-of select="$document_language"/></xsl:otherwise>
                </xsl:choose>
            </xsl:attribute>
            <xsl:apply-templates select="p"/>
        </notebio>
    </xsl:template>

    <xsl:template match="ref" mode="unestructured_unformated">
        <refbiblio>
            <xsl:if test="@id">
                <xsl:attribute name="id">
                    <xsl:value-of select="@id"/>
                </xsl:attribute>
            </xsl:if>
            <xsl:apply-templates select="element-citation/*" mode="unestructured_unformated_elements"/>
        </refbiblio>
    </xsl:template>

    <xsl:template match="*" mode="unestructured_unformated_elements">
        <xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="body">
        <corps>
            <xsl:choose>
                <xsl:when test="count(p) = 1">
                    <texte typetexte="libre"><xsl:value-of select="p" /></texte>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates select="." mode="text_with_formating"/>
                </xsl:otherwise>
            </xsl:choose>
        </corps>
    </xsl:template>

    <xsl:template match="sec">
        <xsl:param name="level"/>
        <xsl:variable name="section_name"><xsl:value-of select="concat('section', $level)"/></xsl:variable>
        <xsl:element name="{$section_name}">
            <xsl:attribute name="id">
                <xsl:value-of select="concat('s',$level,'n', position())"/>
            </xsl:attribute>
            <no><xsl:value-of select="position()"/></no>
            <xsl:apply-templates select="title" mode="elemif">
                <xsl:with-param name="elem_name">titre</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="sec" mode="corps">
                <xsl:with-param name="level"><xsl:value-of select="$level+1"/></xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="p|fig|table-wrap|list"/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="list">
        <xsl:variable name="list-type"><xsl:value-of select="@list-type"/></xsl:variable>

        <xsl:element name="{$reference_tab/reference-tab/group[@value='lists']/key[@value = $list-type]}">
            <!--IMPROVEMENTS: Implement relation list of ordering type, Waiting Texture definitions -->
            <xsl:choose>
                <xsl:when test="$reference_tab/reference-tab/group[@value='lists']/key[@value = $list-type] = 'listeord'">
                    <xsl:attribute name="numeration">decimal</xsl:attribute>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:attribute name="signe">disque</xsl:attribute>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:for-each select="list-item">
                <elemliste>
                    <xsl:apply-templates select="p|fig|table-wrap|list"></xsl:apply-templates>
                </elemliste>
            </xsl:for-each>
        </xsl:element>
    </xsl:template>

    <xsl:template match="fig">
        <figure>
            <xsl:apply-templates select="@id" mode="attrif"/>
            <xsl:if test="label">
                <no><xsl:value-of select="label"/></no>
            </xsl:if>
            <xsl:apply-templates select="caption"/>
            <xsl:apply-templates select="alt-text" mode="figure"/>
            <objetmedia flot="bloc">
                <!--IMPROVEMENT: Verify how the attribute typeimage is used in Érudit, it is hard coded as figure now -->
                <!--IMPROVEMENT: Verify how the attribute xlink:type is used in Érudit, it is hard coded as figure now -->
                <image typeimage="figure" xlink:type="simple">
                    <xsl:attribute name="id"><xsl:value-of select="graphic/@id"/></xsl:attribute>
                    <xsl:attribute name="xlink:href"><xsl:value-of select="graphic/@xlink:href"/></xsl:attribute>
                </image>
            </objetmedia>
            <xsl:apply-templates select="attrib"/>
        </figure>
    </xsl:template>

    <xsl:template match="alt-text" mode="figure">
        <notefig>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </notefig>
    </xsl:template>

    <xsl:template match="front">
        <admin>
            <xsl:apply-templates select="article-meta"/>
            <xsl:apply-templates select="journal-meta"/>
            <xsl:apply-templates select="article-meta" mode="issue"/>
            <xsl:apply-templates select="journal-meta/publisher/publisher-name"/>
            <prodnum><nomorg>Érudit</nomorg></prodnum>
            <diffnum><nomorg>Érudit</nomorg></diffnum>
            <schema nom="Erudit Article" version="3.0.0" lang="fr"/>
            <xsl:apply-templates select="article-meta/permissions"/>
        </admin>
        <liminaire>
            <xsl:apply-templates select="article-meta/title-group"/>
            <xsl:apply-templates select="article-meta/contrib-group" mode="grauteur"/>
            <xsl:apply-templates select="notes/sec[@sec-type='article-note']" mode="article-note"/>
            <xsl:apply-templates select="article-meta/abstract"/>
            <xsl:apply-templates select="article-meta/trans-abstract"/>
            <xsl:apply-templates select="article-meta/kwd-group"/>
        </liminaire>
    </xsl:template>

    <xsl:template match="journal-meta">
        <revue>
            <xsl:if test="journal-id[@journal-id-type='publisher-id']">
                <xsl:attribute name="id">
                    <xsl:value-of select="journal-id[@journal-id-type='publisher-id']"/>
                </xsl:attribute>
            </xsl:if>
            <xsl:apply-templates select="journal-title-group/journal-title"/>
            <xsl:apply-templates select="journal-title-group/journal-subtitle"/>
            <xsl:apply-templates select="journal-title-group/trans-title-group" mode="paral"/>
            <xsl:apply-templates select="journal-title-group/abbrev-journal-title"/>
            <xsl:apply-templates select="issn[@pub-type='ppub']"/>
            <xsl:apply-templates select="issn[@pub-type='epub']"/>
            <xsl:apply-templates select="contrib-group[@content-type='manager']/contrib" mode="board"/>
            <xsl:apply-templates select="contrib-group[@content-type='editor']/contrib" mode="board"/>
        </revue>
    </xsl:template>

    <xsl:template match="journal-title">
        <titrerev>
            <xsl:value-of select="."/>
        </titrerev>
    </xsl:template>

    <xsl:template match="journal-subtitle">
        <sstitrerev>
            <xsl:value-of select="."/>
        </sstitrerev>
    </xsl:template>

    <xsl:template match="abbrev-journal-title">
        <titrerevabr>
            <xsl:value-of select="."/>
        </titrerevabr>
    </xsl:template>

    <xsl:template match="trans-title-group" mode="paral">
        <xsl:apply-templates select="trans-title"/>
        <xsl:apply-templates select="trans-subtitle"/>
    </xsl:template>

    <xsl:template match="trans-title">
        <titrerevparal>
            <xsl:attribute name="lang"><xsl:value-of select="../@xml:lang"/></xsl:attribute>
            <xsl:value-of select="."/>
        </titrerevparal>
    </xsl:template>

    <xsl:template match="trans-subtitle">
        <sstitrerevparal>
            <xsl:attribute name="lang"><xsl:value-of select="../@xml:lang"/></xsl:attribute>
            <xsl:value-of select="."/>
        </sstitrerevparal>
    </xsl:template>

    <xsl:template match="article-meta">
        <infoarticle>
            <xsl:apply-templates select="article-id[@pub-id-type='doi']"/>
            <xsl:if test="fpage | lpage">
                <pagination>
                    <xsl:apply-templates select="fpage" mode="elemif">
                        <xsl:with-param name="elem_name">ppage</xsl:with-param>
                    </xsl:apply-templates>
                    <xsl:apply-templates select="lpage" mode="elemif">
                        <xsl:with-param name="elem_name">dpage</xsl:with-param>
                    </xsl:apply-templates>
                </pagination>
            </xsl:if>
            <xsl:if test="(fpage and lpage) and (lpage >= fpage)">
                <nbpage>
                    <xsl:value-of select="(lpage - fpage) + 1"/>
                </nbpage>
            </xsl:if>
            <nbpara>
                <xsl:value-of select="count(../../body//p)"/>
            </nbpara>
            <nbmot>
                <!-- '&#x20;&#xD;&#xA;&#x9;' = supported word spaces for word counting -->
                <xsl:value-of select="count(str:tokenize(string(../../body), '&#x20;&#xD;&#xA;&#x9;'))"/>
            </nbmot>
            <nbfig>
                <xsl:value-of select="count(../../body//fig | ../../partiesann//fig)"/>
            </nbfig>
            <nbtabl>
                <xsl:value-of select="count(../../body//table-wrap | ../../partiesann//table-wrap)"/>
            </nbtabl>
            <nbeq>
                <xsl:value-of select="count(../../body//disp-formula | ../../partiesann//dispformula)"/>
            </nbeq>
            <nbom>
                <xsl:value-of select="count(../../body//media | ../../partiesann//media)"/>
            </nbom>
            <nbimage>
                <xsl:value-of select="count(../../body//graphic | ../../partiesann//graphic)"/>
            </nbimage>
            <nbaudio>
                <xsl:value-of select="count(../corps//media[@mimetype='audio'] | ../partiesann//media[@mimetype='audio'])"/>
            </nbaudio>
            <nbvideo>
                <xsl:value-of select="count(../corps//media[@mimetype='video'] | ../partiesann//media[@mimetype='video'])"/>
            </nbvideo>
            <nbrefbiblio>
                <xsl:value-of select="count(//ref)"/>
            </nbrefbiblio>
            <nbnote>
                <xsl:value-of select="count(//fn)"/>
            </nbnote>
        </infoarticle>
    </xsl:template>

    <xsl:template match="article-meta" mode="issue">
        <numero>
            <xsl:attribute name="id">
                <xsl:value-of select="issue-id[@pub-id-type='publisher-id']"/>
            </xsl:attribute>
            <xsl:apply-templates select="volume" mode="elemif"/>
            <xsl:apply-templates select="issue" mode="elemif">
                <xsl:with-param name="elem_name">nonumero</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="pub-date[@date-type='collection']" mode="pub" />
            <xsl:apply-templates select="pub-date[@date-type='pub']" mode="pubnum" />
            <xsl:apply-templates select="issue-title" />
            <xsl:apply-templates select="../notes/sec[@sec-type='issue-note']" mode="issue-note"/>
        </numero>
    </xsl:template>

    <xsl:template match="sec" mode="issue-note">
        <notegen porteenoteg="numero">
            <xsl:attribute name="lang">
                <xsl:value-of select="@xml:lang"/>
            </xsl:attribute>
            <xsl:apply-templates select="title"/>
            <xsl:apply-templates select="p"/>
        </notegen>
    </xsl:template>

    <xsl:template match="sec" mode="article-note">
        <notegen porteenoteg="article">
            <xsl:attribute name="lang">
                <xsl:value-of select="@xml:lang"/>
            </xsl:attribute>
            <xsl:apply-templates select="title"/>
            <xsl:apply-templates select="p"/>
        </notegen>
    </xsl:template>

    <xsl:template match="pub-date" mode="pub">
        <pub>
            <xsl:apply-templates select="season" mode="elemif">
                <xsl:with-param name="elem_name">periode</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="year" mode="elemif">
                <xsl:with-param name="elem_name">annee</xsl:with-param>
            </xsl:apply-templates>
        </pub>
    </xsl:template>

    <xsl:template match="pub-date" mode="pubnum">
        <pubnum>
            <date>
                <xsl:attribute name="typedate">
                    <xsl:call-template name="reference_tab">
                        <xsl:with-param name="group">publication-format</xsl:with-param>
                        <xsl:with-param name="key"><xsl:value-of select="@publication-format"/></xsl:with-param>
                    </xsl:call-template>
                </xsl:attribute>
                <xsl:choose>
                    <xsl:when test="day != ''">
                        <xsl:value-of select="year"/>-<xsl:value-of select="month"/>-<xsl:value-of select="day"/>
                    </xsl:when>
                    <xsl:when test="month != ''">
                        <xsl:value-of select="year"/>-<xsl:value-of select="month"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="year"/>
                    </xsl:otherwise>
                </xsl:choose>
            </date>
        </pubnum>
    </xsl:template>

    <xsl:template match="issue-title">
        <grtheme>
            <theme><xsl:value-of select="."/></theme>
        </grtheme>
    </xsl:template>

    <xsl:template match="title-group">
        <grtitre>
            <xsl:apply-templates select="../article-categories//subj-group"/>
            <xsl:apply-templates select="article-title"/>
            <xsl:apply-templates select="subtitle"/>
            <xsl:apply-templates select="../product/related-object" mode="trefbiblio"/>
            <xsl:apply-templates select="trans-title-group"/>
            <!--IMPROVEMENT: To find a co-relation in JATS4M for surtitreparal -->
            <!--surtitreparal lang="fr"/-->
        </grtitre>
    </xsl:template>

    <xsl:template match="related-object" mode="trefbiblio">
        <trefbiblio><xsl:apply-templates select="." mode="text_with_formating"/></trefbiblio>
    </xsl:template>

    <xsl:template match="article-title">
        <titre>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </titre>
    </xsl:template>

    <xsl:template match="subtitle">
        <sstitre>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </sstitre>
    </xsl:template>

    <xsl:template match="trans-title-group">
        <xsl:apply-templates select="trans-title"/>
        <xsl:apply-templates select="trans-subtitle"/>
    </xsl:template>

    <xsl:template match="trans-title">
        <titreparal>
            <xsl:attribute name="lang">
                <xsl:value-of select="../@xml:lang"/>
            </xsl:attribute>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </titreparal>
    </xsl:template>

    <xsl:template match="trans-subtitle">
        <sstitreparal>
            <xsl:attribute name="lang">
                <xsl:value-of select="../@xml:lang"/>
            </xsl:attribute>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </sstitreparal>
    </xsl:template>

    <xsl:template match="subj-group">
        <xsl:variable name="elemindex">
            <xsl:choose>
                <xsl:when test="../../article-categories"/>
                <xsl:when test="../../../article-categories">2</xsl:when>
                <xsl:otherwise>3</xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <xsl:variable name="surtitre_type">
            <xsl:if test="@xml:lang!=$document_language">paral</xsl:if>
        </xsl:variable>
        <xsl:variable name="elemname" select="concat('surtitre', $surtitre_type, $elemindex)"/>
        <xsl:element name="{$elemname}">
            <xsl:if test="@xml:lang">
                <xsl:attribute name="lang"><xsl:value-of select="@xml:lang"/></xsl:attribute>
            </xsl:if>
            <xsl:value-of select="subject"/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="contrib-group" mode="grauteur">
        <grauteur>
            <xsl:apply-templates select="contrib" mode="auteur"></xsl:apply-templates>
        </grauteur>
    </xsl:template>

    <xsl:template match="contrib" mode="board">
        <xsl:variable name="contrib-type">
            <xsl:call-template name="reference_tab">
                <xsl:with-param name="group">contrib-type</xsl:with-param>
                <xsl:with-param name="key"><xsl:value-of select="../@content-type"/></xsl:with-param>
            </xsl:call-template>
        </xsl:variable>
        <xsl:element name="{$contrib-type}">
            <xsl:if test="role and $contrib-type='redacteurchef'">
                <xsl:attribute name="typerc">
                    <xsl:call-template name="reference_tab">
                        <xsl:with-param name="group">role</xsl:with-param>
                        <xsl:with-param name="key"><xsl:value-of select="role"/></xsl:with-param>
                    </xsl:call-template>
                </xsl:attribute>
            </xsl:if>
            <xsl:apply-templates select="@contrib-type"/>
            <xsl:apply-templates select="collab/named-content[@content-type='name']" mode="elemif">
                <xsl:with-param name="elem_name">nomorg</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="name"/>
            <xsl:apply-templates select="xref" mode="affiliation"/>
            <xsl:apply-templates select="email" mode="elemif">
                <xsl:with-param name="elem_name">courriel</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="ext-link" mode="grauteur"/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="ext-link" mode="grauteur">
        <siteweb>
            <xsl:value-of select="@xlink:href"/>
        </siteweb>
    </xsl:template>

    <xsl:template match="@contrib-type">
        <fonction>
            <!--IMPROVEMENTS: Check if lang attribute have usage and if not turns it not mandatory in XSD, if it is necessary, check how correctly define it's value -->
            <xsl:attribute name="lang">en</xsl:attribute>
            <xsl:value-of select="."/>
        </fonction>
    </xsl:template>

    <xsl:template match="contrib" mode="auteur">
        <auteur>
            <xsl:attribute name="id">
                <xsl:value-of select="@id"/>
            </xsl:attribute>
            <xsl:choose>
                <xsl:when test="contrib-id">
                    <xsl:apply-templates select="." mode="autorite"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates select="." mode="not_autorite"/>
                </xsl:otherwise>
            </xsl:choose>
        </auteur>
    </xsl:template>

    <xsl:template match="*" mode="not_autorite">
        <xsl:apply-templates select="collab/named-content[@content-type='name']" mode="org-name"/>
        <xsl:apply-templates select="collab/contrib-group/contrib" mode="org-members"/>
        <xsl:apply-templates select="name"/>
        <xsl:apply-templates select="xref" mode="affiliation"/>
        <xsl:apply-templates select="email" mode="elemif">
            <xsl:with-param name="elem_name">courriel</xsl:with-param>
        </xsl:apply-templates>
        <xsl:apply-templates select="ext-link" mode="grauteur"/>
    </xsl:template>

    <xsl:template match="*" mode="autorite">
        <autorite>
            <xsl:attribute name="cleautorite"><xsl:value-of select="contrib-id"/></xsl:attribute>
            <xsl:apply-templates select="collab/named-content[@content-type='name']" mode="org-name"/>
            <xsl:apply-templates select="collab/contrib-group/contrib" mode="org-members"/>
            <xsl:apply-templates select="name"/>
            <xsl:apply-templates select="xref" mode="affiliation"/>
            <xsl:apply-templates select="email" mode="elemif">
                <xsl:with-param name="elem_name">courriel</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="ext-link" mode="grauteur"/>
        </autorite>
    </xsl:template>

    <xsl:template match="xref" mode="affiliation">
        <xsl:variable name="rid" select="@rid"/>
        <affiliation>
            <alinea>
                <xsl:value-of select="//aff[@id=$rid]"/>
            </alinea>
        </affiliation>
    </xsl:template>

    <xsl:template match="contrib" mode="org-members">
        <membre>
            <xsl:apply-templates select="name"/>
            <xsl:apply-templates select="xref" mode="affiliation"/>
            <xsl:apply-templates select="email" mode="elemif">
                <xsl:with-param name="elem_name">courriel</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="ext-link" mode="grauteur"/>
        </membre>
    </xsl:template>

    <xsl:template match="name">
        <nompers>
            <xsl:apply-templates select="given-names"/>
            <xsl:apply-templates select="surname" mode="elemif">
                <xsl:with-param name="elem_name">nomfamille</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="prefix" mode="elemif">
                <xsl:with-param name="elem_name">prefixe</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="suffix" mode="elemif">
                <xsl:with-param name="elem_name">suffixe</xsl:with-param>
            </xsl:apply-templates>
        </nompers>
    </xsl:template>

    <xsl:template match="given-names">
        <xsl:variable name="firstname" select="substring-before(., ' ')"/>
        <xsl:variable name="secondname" select="substring-after(., ' ')"/>
        <prenom>
            <xsl:choose>
                <xsl:when test="$firstname!=''"><xsl:value-of select="$firstname"/></xsl:when>
                <xsl:otherwise><xsl:value-of select="."/></xsl:otherwise>
            </xsl:choose>
        </prenom>
        <xsl:if test="$secondname!=''">
            <autreprenom>
                <xsl:value-of select="$secondname"/>
            </autreprenom>
        </xsl:if>
    </xsl:template>

    <xsl:template match="aff">
        <affiliation>
            <alinea>
                <xsl:value-of select="."/>
            </alinea>
        </affiliation>
    </xsl:template>

    <xsl:template match="named-content" mode="org-name">
        <nomorg>
            <xsl:value-of select="."/>
        </nomorg>
    </xsl:template>

    <xsl:template match="abstract">
        <resume>
            <xsl:attribute name="lang">
                <xsl:value-of select="$document_language"/>
            </xsl:attribute>
            <xsl:apply-templates select="title"/>
            <xsl:apply-templates select="p"/>
        </resume>
    </xsl:template>

    <xsl:template match="title">
        <titre>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </titre>
    </xsl:template>

    <xsl:template match="trans-abstract">
        <resume>
            <xsl:attribute name="lang"><xsl:value-of select="@xml:lang"/></xsl:attribute>
            <xsl:apply-templates select="title"/>
            <xsl:apply-templates select="p"/>
        </resume>
    </xsl:template>

    <xsl:template match="kwd-group">
        <grmotcle>
            <xsl:apply-templates select="@xml:lang" mode="attrif">
                <xsl:with-param name="attr_name">lang</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="title"/>
            <xsl:apply-templates select="kwd"/>
        </grmotcle>
    </xsl:template>

    <xsl:template match="kwd">
        <motcle>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </motcle>
    </xsl:template>

    <xsl:template match="article-id">
        <idpublic>
            <xsl:attribute name="scheme">
                <xsl:call-template name="reference_tab">
                    <xsl:with-param name="group">pub-id-type</xsl:with-param>
                    <xsl:with-param name="key"><xsl:value-of select="@pub-id-type"/></xsl:with-param>
                </xsl:call-template>
            </xsl:attribute>
            <xsl:value-of select="."/>
        </idpublic>
    </xsl:template>

    <xsl:template match="issn[@pub-type='epub']">
        <idissnnum><xsl:value-of select="."/></idissnnum>
    </xsl:template>

    <xsl:template match="issn[@pub-type='ppub']">
        <idissn><xsl:value-of select="."/></idissn>
    </xsl:template>

    <xsl:template match="publisher-name">
        <editeur>
            <nomorg><xsl:value-of select="."/></nomorg>
        </editeur>
    </xsl:template>

    <xsl:template match="permissions">
        <droitsauteur>
            <xsl:apply-templates select="copyright-statement"/>
            <xsl:apply-templates select="copyright-year"/>
            <xsl:apply-templates select="copyright-holder"/>
        </droitsauteur>
        <xsl:apply-templates select="license"/>
    </xsl:template>

    <xsl:template match="copyright-statement">
        <declaration>
            <xsl:value-of select="."/>
        </declaration>
    </xsl:template>

    <xsl:template match="copyright-year">
        <annee>
            <xsl:value-of select="."/>
        </annee>
    </xsl:template>

    <xsl:template match="copyright-holder">
        <nomorg>
            <xsl:value-of select="."/>
        </nomorg>
    </xsl:template>

    <xsl:template match="license">
        <droitsauteur>
            <xsl:if test="@xlink:href">
                <liensimples>
                    <xsl:attribute name="xlink:href"><xsl:value-of select="@xlink:href"/></xsl:attribute>
                </liensimples>
            </xsl:if>
            <xsl:apply-templates select="license-p"/>
        </droitsauteur>
    </xsl:template>

    <xsl:template match="license-p">
        <xsl:apply-templates select="." mode="text_with_formating"/>
    </xsl:template>

    <xsl:template match="graphic">
        <xsl:param name="typeimage"/>
        <objetmedia>
            <xsl:attribute name="float">ligne</xsl:attribute>
            <image typeimage="{$typeimage}">
                <xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
                <xsl:attribute name="xlink:href"><xsl:value-of select="@xlink:href"/></xsl:attribute>
            </image>
        </objetmedia>
    </xsl:template>

    <xsl:template match="boxed-text[@content-type='frame']">
        <encadre>
            <xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
            <xsl:apply-templates select="*"/>
        </encadre>
    </xsl:template>

    <xsl:template match="boxed-text/sec">
        <section1><xsl:apply-templates select="*"/></section1>
    </xsl:template>

    <xsl:template match="boxed-text/sec/p">
        <alinea><xsl:apply-templates select="." mode="text_with_formating"/></alinea>
    </xsl:template>

    <xsl:template match="p" mode="para">
        <!--IMPROVEMENT: Fix the pharagrafs count, it is counting any p element inside the XML, but needs to count only those child of sec-->
        <xsl:variable name="pcount">
            <xsl:value-of select="count(preceding::corpus/p)" />
        </xsl:variable>
        <para>
            <xsl:attribute name="id">
                <xsl:value-of select="concat('pa', $pcount)"/>
            </xsl:attribute>
            <no><xsl:value-of select="concat('pa', $pcount)"/></no>
            <alinea>
                <xsl:apply-templates select="." mode="text_with_formating"/>
            </alinea>
        </para>
    </xsl:template>

    <xsl:template match="sc">
        <marquage typemarq="petitecap">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </marquage>
    </xsl:template>

    <xsl:template match="styled-content[@style-type='text-uppercase']">
        <marquage typemarq="majuscule">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </marquage>
    </xsl:template>

    <xsl:template match="styled-content[@style-type='text-boxed']">
        <marquage typemarq="filet">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </marquage>
    </xsl:template>

    <xsl:template match="styled-content[@style-type='text-bigger']">
        <marquage typemarq="tailleg">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </marquage>
    </xsl:template>

    <xsl:template match="styled-content[@style-type='text-smaller']">
        <marquage typemarq="taillep">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </marquage>
    </xsl:template>

    <xsl:template match="strike">
        <marquage typemarq="barre">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </marquage>
    </xsl:template>

    <xsl:template match="monospace">
        <marquage typemarq="espacefixe">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </marquage>
    </xsl:template>

    <xsl:template match="overline">
        <marquage typemarq="surlignage">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </marquage>
    </xsl:template>

    <xsl:template match="underline">
        <marquage typemarq="souligne">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </marquage>
    </xsl:template>

    <xsl:template match="italic">
        <marquage typemarq="italique">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </marquage>
    </xsl:template>

    <xsl:template match="bold">
        <marquage typemarq="gras">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </marquage>
    </xsl:template>

    <xsl:template match="sub">
        <indice>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </indice>
    </xsl:template>

    <xsl:template match="sup">
        <exposant>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </exposant>
    </xsl:template>

    <xsl:template match="xref">
        <!--IMPROVEMENT: fix the @rid value, cleaning any other caracter != number -->
        <xsl:variable name="relno">
            <xsl:value-of select="concat('rel', @rid)"/>
        </xsl:variable>
        <xsl:variable name="no">
            <xsl:value-of select="@rid"/>
        </xsl:variable>
        <renvoi id="{$relno}" idref="{$no}" typeref="note">
            <xsl:value-of select="."/>
        </renvoi>
    </xsl:template>

    <xsl:template match="disp-quote[@content-type='epigraph']">
        <epigraphe>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </epigraphe>
    </xsl:template>

    <xsl:template match="disp-quote[@content-type='dedication']">
        <dedicace>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </dedicace>
    </xsl:template>

    <xsl:template match="disp-quote[@content-type='verbatim']">
        <verbatim>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </verbatim>
    </xsl:template>

    <xsl:template match="disp-formula-group">
        <grequation>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </grequation>
    </xsl:template>

    <xsl:template match="disp-formula">
        <equation>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </equation>
    </xsl:template>

    <xsl:template match="table-wrap-group">
        <grtableau>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </grtableau>
    </xsl:template>

    <xsl:template match="table-wrap">
        <tableau>
            <xsl:apply-templates select="@id" mode="attrif"/>
            <xsl:apply-templates select="label|caption"/>
            <xsl:apply-templates select="table-wrap-foot/fn-group/fn" mode="table"/>
            <xsl:apply-templates select="graphic">
                <xsl:with-param name="typeimage">tableau</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="table"/>
            <xsl:apply-templates select="table-wrap-foot/attrib"/>
        </tableau>
    </xsl:template>

    <xsl:template match="fn" mode="table">
        <notetabl>
            <xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
            <xsl:apply-templates select="p/." mode="text_with_formating"/>
        </notetabl>
    </xsl:template>


    <xsl:template match="table">
        <tabtexte>
            <xsl:apply-templates select="colgroup"/>
            <xsl:apply-templates select="thead"/>
            <xsl:apply-templates select="tbody"/>
            <xsl:apply-templates select="tfoot"/>
        </tabtexte>
    </xsl:template>

    <xsl:template match="colgroup">
        <tabgrcol>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </tabgrcol>
    </xsl:template>

    <xsl:template match="col">
        <tabcol>
            <xsl:if test="@align">
                <xsl:attribute name="alignh">
                    <xsl:call-template name="reference_tab">
                        <xsl:with-param name="group">table-cel-halign</xsl:with-param>
                        <xsl:with-param name="key">
                            <xsl:value-of select="@align"/>
                        </xsl:with-param>
                    </xsl:call-template>
                </xsl:attribute>
            </xsl:if>
            <xsl:if test="@valign">
                <xsl:attribute name="alignv">
                    <xsl:call-template name="reference_tab">
                        <xsl:with-param name="group">table-cel-valign</xsl:with-param>
                        <xsl:with-param name="key">
                            <xsl:value-of select="@valign"/>
                        </xsl:with-param>
                    </xsl:call-template>
                </xsl:attribute>
            </xsl:if>
            <xsl:if test="@char">
                <xsl:attribute name="caraca"><xsl:value-of select="@char"/></xsl:attribute>
            </xsl:if>
            <xsl:if test="@span">
                <xsl:attribute name="nbcol"><xsl:value-of select="@span"/></xsl:attribute>
            </xsl:if>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </tabcol>
    </xsl:template>

    <xsl:template match="thead">
        <tabentete>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </tabentete>
    </xsl:template>


    <xsl:template match="tfoot">
        <tabpied>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </tabpied>
    </xsl:template>

    <xsl:template match="tbody">
        <tabgrligne>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </tabgrligne>
    </xsl:template>

    <xsl:template match="tr">
        <tabligne>
            <xsl:apply-templates select="th">
                <xsl:with-param name="style">tabcellulee</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="td">
                <xsl:with-param name="style">tabcelluled</xsl:with-param>
            </xsl:apply-templates>
        </tabligne>
    </xsl:template>

    <xsl:template match="th">
        <tabcellulee>
            <alinea>
                <xsl:apply-templates select="td" mode="text_with_formating"/>
            </alinea>
        </tabcellulee>
    </xsl:template>

    <xsl:template match="td|th">
        <xsl:param name="style"/>
        <xsl:variable name="pos" select="position()"/>
        <xsl:variable name="general-halign"
            select="../../../colgroup//col[position() = $pos]/@align"/>
        <xsl:variable name="general-valign"
            select="../../../colgroup//col[position() = $pos]/@valign"/>
        <xsl:element name="{$style}">
            <xsl:if test="@align">
                <xsl:attribute name="alignh">
                    <xsl:call-template name="reference_tab">
                        <xsl:with-param name="group">table-cel-halign</xsl:with-param>
                        <xsl:with-param name="key">
                            <xsl:value-of select="@align"/>
                        </xsl:with-param>
                    </xsl:call-template>
                </xsl:attribute>
            </xsl:if>
            <xsl:if test="@valign">
                <xsl:attribute name="alignv">
                    <xsl:call-template name="reference_tab">
                        <xsl:with-param name="group">table-cel-valign</xsl:with-param>
                        <xsl:with-param name="key">
                            <xsl:value-of select="@valign"/>
                        </xsl:with-param>
                    </xsl:call-template>
                </xsl:attribute>
            </xsl:if>
            <xsl:if test="@char">
                <xsl:attribute name="carac"><xsl:value-of select="@char"/></xsl:attribute>
            </xsl:if>
            <xsl:if test="@rowspan">
                <xsl:attribute name="nbligne"><xsl:value-of select="@rowspan"/></xsl:attribute>
            </xsl:if>
            <xsl:if test="@colspan">
                <xsl:attribute name="nbcol"><xsl:value-of select="@colspan"/></xsl:attribute>
            </xsl:if>
            <xsl:if test="@align != '' or $general-halign != ''">
                <xsl:attribute name="alignh">
                    <xsl:choose>
                        <xsl:when test="@align">
                            <xsl:call-template name="reference_tab">
                                <xsl:with-param name="group">table-cel-halign</xsl:with-param>
                                <xsl:with-param name="key">
                                    <xsl:value-of select="@align"/>
                                </xsl:with-param>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:when test="$general-halign != ''">
                            <xsl:call-template name="reference_tab">
                                <xsl:with-param name="group">table-cel-halign</xsl:with-param>
                                <xsl:with-param name="key">
                                    <xsl:value-of select="$general-halign"/>
                                </xsl:with-param>
                            </xsl:call-template>
                        </xsl:when>
                    </xsl:choose>
                </xsl:attribute>
            </xsl:if>
            <xsl:if test="@valign != '' or $general-valign != ''">
                <xsl:attribute name="alignv">
                    <xsl:choose>
                        <xsl:when test="@valign">
                            <xsl:call-template name="reference_tab">
                                <xsl:with-param name="group">table-cel-valign</xsl:with-param>
                                <xsl:with-param name="key">
                                    <xsl:value-of select="@valign"/>
                                </xsl:with-param>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:when test="$general-valign != ''">
                            <xsl:call-template name="reference_tab">
                                <xsl:with-param name="group">table-cel-valign</xsl:with-param>
                                <xsl:with-param name="key">
                                    <xsl:value-of select="$general-valign"/>
                                </xsl:with-param>
                            </xsl:call-template>
                        </xsl:when>
                    </xsl:choose>
                </xsl:attribute>
            </xsl:if>
            <alinea>
                <xsl:apply-templates select="." mode="text_with_formating"/>
            </alinea>
        </xsl:element>
    </xsl:template>

    <xsl:template match="caption">
        <legende>
            <xsl:apply-templates select="@xml:lang" mode="attrif">
                <xsl:with-param name="attr_name">lang</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </legende>
    </xsl:template>

    <xsl:template match="sec">
        <section1>
            <xsl:apply-templates select="*" mode="sec"/>
        </section1>
    </xsl:template>

    <xsl:template match="sec/sec">
        <section2>
            <xsl:apply-templates select="*" mode="sec"/>
        </section2>
    </xsl:template>

    <xsl:template match="sec/sec/sec">
        <section3>
            <xsl:apply-templates select="*" mode="sec"/>
        </section3>
    </xsl:template>

    <xsl:template match="sec/sec/sec/sec">
        <section4>
            <xsl:apply-templates select="*" mode="sec"/>
        </section4>
    </xsl:template>

    <xsl:template match="sec/sec/sec/sec/sec">
        <section5>
            <xsl:apply-templates select="*" mode="sec"/>
        </section5>
    </xsl:template>

    <xsl:template match="sec/sec/sec/sec/sec/sec">
        <section6>
            <xsl:apply-templates select="*" mode="sec"/>
        </section6>
    </xsl:template>

    <xsl:template match="mml:math">
        <xsl:copy-of select="."/>
    </xsl:template>

    <xsl:template match="*" mode="sec">
        <xsl:choose>
            <xsl:when test="name(.)='p'">
                <xsl:apply-templates select="." mode="para"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="."/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="label">
        <no>
            <xsl:value-of select="."/>
        </no>
    </xsl:template>

    <xsl:template match="p">
        <alinea>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </alinea>
    </xsl:template>

    <xsl:template match="attrib">
        <source>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </source>
    </xsl:template>

    <xsl:template match="* | text()" mode="text_with_formating">
        <xsl:apply-templates select="* | text()"/>
    </xsl:template>

    <xsl:template match="* | @*">
        <PENDING-TREATMENT>
            <xsl:copy-of select="."/>
        </PENDING-TREATMENT>
    </xsl:template>
 
</xsl:stylesheet>