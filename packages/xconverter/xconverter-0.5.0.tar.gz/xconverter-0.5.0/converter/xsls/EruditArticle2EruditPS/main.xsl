<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    xmlns:str="http://exslt.org/strings"
    xmlns:converter="converter"
    exclude-result-prefixes="converter xsi xs xlink mml str"
    version="2.0">

    <xsl:import href="utils.xsl"/>
    
    <xsl:output method="xml" encoding="utf-8" omit-xml-declaration="yes" indent="yes"/>
   
    <xsl:variable name="affiliations">
        <xsl:for-each select="//affiliation[not(preceding::affiliation/. = .)]">
            <aff>
                <xsl:attribute name="id">aff<xsl:value-of select="position()"/></xsl:attribute>
                <institution>
                    <xsl:attribute name="content-type">orgname</xsl:attribute>
                    <xsl:value-of select="."/>
                </institution>
            </aff>
        </xsl:for-each>
    </xsl:variable>

    <xsl:variable name="document_language" select="substring(/article/@lang,1,2)"/>
    <xsl:variable name="grtheme_id" select="/article/@idref"/>

    <xsl:template match="article">
        <article xmlns="https://jats.nlm.nih.gov/archiving/1.2">
            <xsl:attribute name="dtd-version">1.2</xsl:attribute>
            <xsl:attribute name="specific-use">eps-0.2</xsl:attribute>
            <xsl:attribute name="article-type">
                <xsl:call-template name="reference_tab">
                    <xsl:with-param name="group">article-type</xsl:with-param>
                    <xsl:with-param name="key">
                        <xsl:value-of select="@typeart"/>
                    </xsl:with-param>
                </xsl:call-template>
            </xsl:attribute>
            <xsl:attribute name="xml:lang">
                <xsl:value-of select="$document_language"/>
            </xsl:attribute>
            <front>
                <xsl:apply-templates select="admin/revue"/>
                <xsl:apply-templates select="liminaire"/>
                <xsl:if test="admin/numero/notegen or admin/liminaire/notegen">
                    <notes>
                        <xsl:apply-templates select="admin/numero/notegen" mode="notegen_issue"/>
                        <xsl:apply-templates select="liminaire/notegen" mode="notegen_article"/>
                    </notes>
                </xsl:if>
            </front>
            <xsl:apply-templates select="corps"/>
            <xsl:if test="partiesann">
                <xsl:call-template name="back">
                    <xsl:with-param name="partiesann" select="partiesann"/>
                </xsl:call-template>
            </xsl:if>
        </article>
    </xsl:template>

    <xsl:template match="notegen" mode="notegen_issue">
        <sec sec-type="issue-note">
            <xsl:attribute name="xml:lang">
                <xsl:value-of select="@lang"/>
            </xsl:attribute>
            <xsl:apply-templates select="titre"/>
            <xsl:apply-templates select="alinea" mode="paragraph"/>
        </sec>
    </xsl:template>

    <xsl:template match="notegen" mode="notegen_article">
        <sec sec-type="article-note">
            <xsl:attribute name="xml:lang">
                <xsl:value-of select="@lang"/>
            </xsl:attribute>
            <xsl:apply-templates select="titre"/>
            <xsl:apply-templates select="alinea" mode="paragraph"/>
        </sec>
    </xsl:template>

    <xsl:template name="back">
        <xsl:param name="partiesann"/>
        <back>
            <xsl:apply-templates select="$partiesann/merci"/>
            <xsl:apply-templates select="$partiesann/grnote"/>
            <xsl:apply-templates select="$partiesann/grbiblio/biblio"/>
            <xsl:apply-templates select="$partiesann/grannexe/annexe"/>
        </back>
    </xsl:template>

    <xsl:template match="corps">
        <body>
            <xsl:apply-templates select="*"/>
        </body>
    </xsl:template>

    <xsl:template match="section1 | section2 | section3 | section4 | section5 | section6">
        <sec>
            <xsl:apply-templates select="*"/>
        </sec>
    </xsl:template>

    <xsl:template match="no">
        <xsl:variable name="parent" select="substring(name(..),1,3)"/>
        <xsl:if test="$parent != 'par'">
            <label>
                <xsl:value-of select="."/>
            </label>
        </xsl:if>
    </xsl:template>

    <xsl:template match="alinea">
        <p>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </p>
    </xsl:template>

    <xsl:template match="partiesann"/>

    <xsl:template match="merci">
        <ack>
            <xsl:apply-templates select="titre" mode="elemif">
                <xsl:with-param name="elem_name">title</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="alinea" mode="paragraph"/>
        </ack>
    </xsl:template>

    <xsl:template match="annexe">
        <notes notes-type="annex">
            <xsl:apply-templates select="*"/>
        </notes>
    </xsl:template>

    <xsl:template match="grnote">
        <fn-group>
            <xsl:apply-templates select="note"/>
        </fn-group>
    </xsl:template>

    <xsl:template match="note">
        <fn>
            <xsl:attribute name="id">
                <xsl:value-of select="@id"/>
            </xsl:attribute>
            <xsl:apply-templates select="no"/>
            <xsl:apply-templates select="*" mode="fn"/>
        </fn>
    </xsl:template>


    <xsl:template match="*" mode="fn">
        <xsl:choose>
            <xsl:when test="name(.)='alinea'">
                <xsl:apply-templates select="." mode="paragraph"/>
            </xsl:when>
            <xsl:otherwise>
                <p>
                    <xsl:apply-templates select="."/>
                </p>
            </xsl:otherwise>
        </xsl:choose>   
    </xsl:template>
    
    <xsl:template match="no" mode="fn"/>

    <xsl:template match="biblio">
        <ref-list>
            <xsl:apply-templates select="titre" mode="elemif">
                <xsl:with-param name="elem_name">title</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="refbiblio | divbiblio/refbiblio"/>
        </ref-list>
    </xsl:template>

    <xsl:template match="refbiblio">
        <ref>
            <xsl:if test="@id">
                <xsl:attribute name="id">
                    <xsl:value-of select="@id"/>
                </xsl:attribute>
            </xsl:if>
            <element-citation>
                <styled-content specific-use="display">
                    <xsl:apply-templates select="." mode="text_with_formating"/>
                </styled-content>
                <xsl:apply-templates select="idpublic" mode="references"/>
            </element-citation>
        </ref>
    </xsl:template>

    <xsl:template match="numero" mode="issue_data">
        <xsl:variable name="pf">
            <xsl:call-template name="reference_tab">
                <xsl:with-param name="group">publication-format</xsl:with-param>
                <xsl:with-param name="key">
                    <xsl:value-of select="pubnum/date/@typedate"/>
                </xsl:with-param>
            </xsl:call-template>
        </xsl:variable>
        <pub-date>
            <xsl:attribute name="date-type">collection</xsl:attribute>
            <xsl:apply-templates select="pub"/>
        </pub-date>
        <pub-date>
            <xsl:if test="$pf != ''">
                <xsl:attribute name="publication-format">
                    <xsl:value-of select="$pf"/>
                </xsl:attribute>
            </xsl:if>
            <xsl:attribute name="date-type">pub</xsl:attribute>
            <xsl:copy-of select="converter:isodate-to-elements(pubnum/date)"/>
        </pub-date>

        <xsl:apply-templates select="volume" />
        
        <xsl:variable name="issue-number">
            <xsl:value-of select="converter:issue-number(nonumero)"/>
        </xsl:variable>
        
        <xsl:if test="$issue-number != ''">
            <issue>
                <xsl:attribute name="seq">
                    <xsl:value-of select="/article/@ordseq"/>
                </xsl:attribute>
                <xsl:value-of select="$issue-number"/>
            </issue>
        </xsl:if>

        <xsl:apply-templates select="@id" mode="issue-id"/>
        
        <xsl:apply-templates select="grtheme[@id=$grtheme_id]/theme"/>
        <xsl:apply-templates select="../../admin/infoarticle/pagination/ppage" mode="elemif">
            <xsl:with-param name="elem_name">fpage</xsl:with-param>
        </xsl:apply-templates>
        <xsl:apply-templates select="../../admin/infoarticle/pagination/dpage" mode="elemif">
            <xsl:with-param name="elem_name">lpage</xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="@id" mode="issue-id">
        <issue-id pub-id-type="publisher-id">
            <xsl:value-of select="."/>
        </issue-id>
    </xsl:template>

    <xsl:template match="volume">
        <volume>
            <xsl:if test="boolean(../nonumero) = false">
                <xsl:attribute name="seq">
                    <xsl:value-of select="/article/@ordseq"/>
                </xsl:attribute>
            </xsl:if>
            <xsl:value-of select="."/>
        </volume>
    </xsl:template>

    <xsl:template match="theme">
        <issue-title>
            <xsl:attribute name="xml:lang">
                <xsl:choose>
                    <xsl:when test="@lang">
                        <xsl:value-of select="@lang"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="$document_language"/>        
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:attribute>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </issue-title>
    </xsl:template>

    <xsl:template match="pub">
        
        <xsl:variable name="periode">
            <xsl:value-of select="converter:issue-season(periode)"/>
        </xsl:variable>
        
        <xsl:if test="$periode != ''">
            <season>
                <xsl:value-of select="$periode"/>
            </season>
        </xsl:if>

        <xsl:apply-templates select="annee" mode="elemif"><xsl:with-param name="elem_name">year</xsl:with-param></xsl:apply-templates>

    </xsl:template>

    <xsl:template match="revue">
        <journal-meta>
            <xsl:apply-templates select="@id" mode="revue-id-erudit"/>
            <journal-title-group>
                <journal-title>
                    <xsl:value-of select="titrerev"/>
                </journal-title>
                <xsl:apply-templates select="sstitrerev"/>
                <xsl:apply-templates select="titrerevparal"/>
                <xsl:apply-templates select="titrerevabr"/>
            </journal-title-group>
            <xsl:call-template name="contrib-group-manager"/>
            <xsl:call-template name="contrib-group-editor"/>
            <xsl:apply-templates select="idissnnum"/>
            <xsl:apply-templates select="idissn"/>
            <xsl:if test="../editeur">
                <publisher>
                    <xsl:apply-templates select="../editeur"/>
                </publisher>
            </xsl:if>
        </journal-meta>
    </xsl:template>

    <xsl:template match="titrerevparal">
        <xsl:variable name="lang" select="@lang"/>
        <trans-title-group>
            <xsl:attribute name="xml:lang"><xsl:value-of select="@lang"/></xsl:attribute>
            <trans-title><xsl:value-of select="."/></trans-title>
            <xsl:apply-templates select="../sstitrerevparal[@lang = $lang]"/>
        </trans-title-group>
    </xsl:template>

    <xsl:template match="sstitrerevparal">
        <trans-subtitle><xsl:value-of select="."/></trans-subtitle>
    </xsl:template>

    <xsl:template match="editeur">
        <publisher-name>
            <xsl:value-of select="nomorg"/>
        </publisher-name>
    </xsl:template>

    <xsl:template name="contrib-group-manager">
        <xsl:if test="directeur">
            <contrib-group>
                <xsl:attribute name="content-type">manager</xsl:attribute>
                <xsl:apply-templates select="directeur"/>
            </contrib-group>
        </xsl:if>
    </xsl:template>

    <xsl:template name="contrib-group-editor">
        <xsl:if test="redacteurchef[@idrefs = $grtheme_id] or boolean(@idrefs = false)">
            <contrib-group>
                <xsl:attribute name="content-type">editor</xsl:attribute>
                <xsl:apply-templates select="redacteurchef" />
            </contrib-group>
        </xsl:if>
    </xsl:template>

    <xsl:template match="directeur">
        <contrib>
            <xsl:attribute name="contrib-type">person</xsl:attribute>
            <xsl:apply-templates select="nompers"/>
            <role>directeur</role>
        </contrib>
    </xsl:template>

    <xsl:template match="redacteurchef">
        <xsl:if test="@idrefs = $grtheme_id or boolean(@idrefs) = false">
            <contrib>
                <xsl:attribute name="contrib-type">person</xsl:attribute>
                <xsl:apply-templates select="nompers"/>
                <role>
                    <xsl:call-template name="reference_tab">
                        <xsl:with-param name="group">redacteurchef</xsl:with-param>
                        <xsl:with-param name="key">
                            <xsl:value-of select="@typerc"/>
                        </xsl:with-param>
                    </xsl:call-template>
                </role>
            </contrib>
        </xsl:if>
    </xsl:template>

    <xsl:template match="nompers">
        <name>
            <xsl:apply-templates select="nomfamille" mode="elemif">
                <xsl:with-param name="elem_name">surname</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="prenom"/>
            <xsl:apply-templates select="prefixe" mode="elemif">
                <xsl:with-param name="elem_name">prefix</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="suffixe" mode="elemif">
                <xsl:with-param name="elem_name">suffix</xsl:with-param>
            </xsl:apply-templates>
        </name>
    </xsl:template>

    <xsl:template match="nompers[@typenompers='pseudonyme']">
        <xsl:variable name="strname">
            <xsl:apply-templates select="*" mode="stringname"/>
        </xsl:variable>

        <string-name content-type="alias">
            <xsl:value-of select="normalize-space($strname)"/>
        </string-name>
    </xsl:template>

    <xsl:template match="*" mode="stringname">
        <xsl:value-of select="concat(., ' ')"/>
    </xsl:template>

    <xsl:template match="prenom">
        <given-names>
            <xsl:value-of select="."/>
            <xsl:if test="../autreprenom">
                <xsl:value-of select="concat(' ', ../autreprenom)"/>
            </xsl:if>
        </given-names>
    </xsl:template>

    <xsl:template match="liminaire">
        <article-meta>
            <xsl:apply-templates select="../admin/infoarticle/idpublic" mode="article"/>
            <article-id pub-id-type="publisher-id">
                <xsl:value-of select="/article/@idproprio"/>
            </article-id>
            <xsl:apply-templates select="grtitre/surtitre"/>
            <xsl:apply-templates select="grtitre"/>
            <xsl:apply-templates select="grauteur"/>
            <xsl:copy-of select="$affiliations"/>
            <xsl:apply-templates select="../admin/numero" mode="issue_data"/>
            <xsl:apply-templates select="grtitre/trefbiblio"/>
            <xsl:if test="../admin/droitsauteur">
                <permissions>
                    <xsl:apply-templates select="../admin/droitsauteur[1]" mode="copyright-statement"/>
                    <xsl:apply-templates select="../admin/droitsauteur[2]" mode="license"/>
                </permissions>
            </xsl:if>
            <xsl:apply-templates select="resume[@lang = $document_language]"/>
            <xsl:apply-templates select="resume[@lang != $document_language]"/>
            <xsl:apply-templates select="grmotcle"/>
            <counts>
                <count count-type="note">
                    <xsl:attribute name="count">
                        <xsl:value-of select="count(//note)"/>
                    </xsl:attribute>
                </count>
                <count count-type="paragraph">
                    <xsl:attribute name="count">
                        <xsl:value-of select="count(../corps//para)"/>
                    </xsl:attribute>
                </count>
                <count count-type="word">
                    <!-- '&#x20;&#xD;&#xA;&#x9;' = supported word spaces for word counting -->
                    <xsl:attribute name="count">
                        <xsl:value-of
                            select="count(str:tokenize(string(../corps), '&#x20;&#xD;&#xA;&#x9;'))"
                        />
                    </xsl:attribute>
                </count>
                <count count-type="image">
                    <xsl:attribute name="count">
                        <xsl:value-of select="count(../corps//image | ../partiesann//image)"/>
                    </xsl:attribute>
                </count>
                <count count-type="audio">
                    <xsl:attribute name="count">
                        <xsl:value-of select="count(../corps//audio | ../partiesann//audio)"/>
                    </xsl:attribute>
                </count>
                <count count-type="video">
                    <xsl:attribute name="count">
                        <xsl:value-of select="count(../corps//video | ../partiesann//video)"/>
                    </xsl:attribute>
                </count>
                <count count-type="media">
                    <xsl:attribute name="count">
                        <xsl:value-of
                            select="count(../corps//objetmedia | ../partiesann//objetmedia)"/>
                    </xsl:attribute>
                </count>
                <fig-count>
                    <xsl:attribute name="count">
                        <xsl:value-of select="count(../corps//figure | ../partiesann//figure)"/>
                    </xsl:attribute>
                </fig-count>
                <table-count>
                    <xsl:attribute name="count">
                        <xsl:value-of select="count(../corps//tableau | ../partiesann//tableau)"/>
                    </xsl:attribute>
                </table-count>
                <equation-count>
                    <xsl:attribute name="count">
                        <xsl:value-of select="count(../corps//equation | ../partiesann//equation)"/>
                    </xsl:attribute>
                </equation-count>
                <ref-count>
                    <xsl:attribute name="count">
                        <xsl:value-of select="count(//refbiblio)"/>
                    </xsl:attribute>
                </ref-count>
                <xsl:if
                    test="(../admin/infoarticle/pagination/dpage and ../admin/infoarticle/pagination/ppage) and (../admin/infoarticle/pagination/dpage >= ../admin/infoarticle/pagination/ppage)">
                    <page-count>
                        <xsl:attribute name="count">
                            <xsl:value-of
                                select="(../admin/infoarticle/pagination/dpage - ../admin/infoarticle/pagination/ppage) + 1"
                            />
                        </xsl:attribute>
                    </page-count>
                </xsl:if>
            </counts>
        </article-meta>
    </xsl:template>

    <xsl:template match="droitsauteur" mode="copyright-statement">
        <copyright-statement>
            <xsl:value-of select="converter:extract-copyright-statement(.)"/>
        </copyright-statement>
        <copyright-year>
            <xsl:value-of select="converter:extract-license-year(.)"/>
        </copyright-year>
        <copyright-holder>
            <xsl:value-of select="nomorg"/>
        </copyright-holder>
    </xsl:template>

    <xsl:template match="droitsauteur" mode="license">
        <license>
            <xsl:if test="liensimple/@xlink:href">
                <xsl:attribute name="xlink:href">
                    <xsl:value-of select="liensimple/@xlink:href"/>
                </xsl:attribute>
            </xsl:if>
            <license-p>
                <xsl:if test="liensimple/objetmedia/image/@xlink:href">
                    <graphic>
                        <xsl:attribute name="xlink:href">
                            <xsl:value-of
                                select="liensimple/objetmedia/image/@xlink:href"/>
                        </xsl:attribute>
                    </graphic>
                </xsl:if>
                <xsl:value-of select="."/>
            </license-p>
        </license>
    </xsl:template>

    <xsl:template match="resume">
        <xsl:variable name="elem_name">
            <xsl:choose>
                <xsl:when test="@lang = $document_language">abstract</xsl:when>
                <xsl:otherwise>trans-abstract</xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <xsl:element name="{$elem_name}">
            <xsl:attribute name="xml:lang">
                <xsl:value-of select="@lang"/>
            </xsl:attribute>
            <xsl:apply-templates select="*"/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="grmotcle">
        <kwd-group>
            <xsl:attribute name="xml:lang">
                <xsl:value-of select="@lang"/>
            </xsl:attribute>
            <xsl:apply-templates select="titre"/>
            <xsl:apply-templates select="motcle"/>
        </kwd-group>
    </xsl:template>

    <xsl:template match="motcle">
        <kwd>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </kwd>
    </xsl:template>

    <xsl:template match="titre">
        <title>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </title>
    </xsl:template>

    <xsl:template match="grauteur">
        <contrib-group>
            <xsl:attribute name="content-type">author</xsl:attribute>
            <xsl:apply-templates select="auteur"/>
        </contrib-group>
    </xsl:template>

    <xsl:template match="auteur">
        <xsl:choose>
            <xsl:when test="autorite">
                <xsl:apply-templates select="autorite" mode="person"/>
            </xsl:when>
            <xsl:when test="membre or nomorg">
                <xsl:apply-templates select="." mode="collab"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="." mode="person"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="autorite" mode="person">
        <xsl:param name="affs"/>
        <xsl:variable name="id" select="../@id"/>
        <contrib>
            <xsl:attribute name="contrib-type">person</xsl:attribute>
            <xsl:attribute name="id">
                <xsl:value-of select="$id"/>
            </xsl:attribute>
            <xsl:apply-templates select="@cleautorite"/>
            <xsl:apply-templates select="nompers"/>
            <xsl:apply-templates select="//partiesann/grnotebio/notebio[@idrefs = $id]/alinea"
                mode="notebio"/>
            <xsl:apply-templates select="courriel" mode="elemif">
                <xsl:with-param name="elem_name">email</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="siteweb"/>
            <xsl:apply-templates select="affiliation/alinea" mode="xref_affiliation"/>
        </contrib>
    </xsl:template>

    <xsl:template match="@cleautorite">
        <contrib-id contrib-id-type="orcid">
            <xsl:if test="substring(1,5,.) = 'orcid'">
                <xsl:attribute name="contrib-id-type">orcid</xsl:attribute>
            </xsl:if>
            <xsl:value-of select="."/>
        </contrib-id>
    </xsl:template>

    <xsl:template match="auteur" mode="person">
        <xsl:param name="affs"/>
        <xsl:variable name="id" select="@id"/>
        <contrib>
            <xsl:attribute name="contrib-type">person</xsl:attribute>
            <xsl:attribute name="id">
                <xsl:value-of select="$id"/>
            </xsl:attribute>
            <xsl:apply-templates select="@cleautorite"/>
            <xsl:apply-templates select="nompers"/>
            <xsl:apply-templates select="//partiesann/grnotebio/notebio[@idrefs = $id]/alinea"
                mode="notebio"/>
            <xsl:apply-templates select="courriel" mode="elemif">
                <xsl:with-param name="elem_name">email</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="siteweb"/>
            <xsl:apply-templates select="affiliation/alinea" mode="xref_affiliation"/>
        </contrib>
    </xsl:template>

    <xsl:template match="siteweb">
        <ext-link>
            <xsl:attribute name="xlink:href">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </ext-link>
    </xsl:template>

    <xsl:template match="para">
        <xsl:apply-templates select="." mode="text_with_formating"/>
    </xsl:template>
    
    <xsl:template match="alinea" mode="paragraph">
        <p>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </p>
    </xsl:template>

    <xsl:template match="resume/alinea">
        <p>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </p>
    </xsl:template>

    <xsl:template match="alinea" mode="notebio">
        <bio>
            <xsl:attribute name="xml:lang">
                <xsl:value-of select="$document_language"/>
            </xsl:attribute>
            <xsl:apply-templates select="../../titre" mode="elemif">
                <xsl:with-param name="elem_name">title</xsl:with-param>
            </xsl:apply-templates>
            <p>
                <xsl:apply-templates select="." mode="text_with_formating"/>
            </p>
        </bio>
    </xsl:template>

    <xsl:template match="auteur" mode="collab">
        <contrib>
            <xsl:attribute name="contrib-type">group</xsl:attribute>
            <xsl:attribute name="id">
                <xsl:value-of select="@id"/>
            </xsl:attribute>
            <xsl:apply-templates select="nomorg" mode="collab"/>
        </contrib>
    </xsl:template>

    <xsl:template match="alinea" mode="xref_affiliation">
        <xref>
            <xsl:attribute name="ref-type">aff</xsl:attribute>
            <xsl:attribute name="rid">
                <xsl:value-of select="converter:get-xref-id(*/text()|./text(), $affiliations)"/>
            </xsl:attribute>
        </xref>
    </xsl:template>

    <xsl:template match="nomorg" mode="collab">
        <collab>
            <named-content>
                <xsl:attribute name="content-type">name</xsl:attribute>
                <xsl:value-of select="."/>
            </named-content>
            <xsl:if test="../membre">
                <contrib-group>
                    <xsl:apply-templates select="../membre" mode="collab">
                        <xsl:with-param name="collab_id">
                            <xsl:value-of select="../@id"/>
                        </xsl:with-param>
                    </xsl:apply-templates>
                </contrib-group>
            </xsl:if>
        </collab>
    </xsl:template>

    <xsl:template match="membre" mode="collab">
        <xsl:param name="collab_id"/>
        <xsl:variable name="ndx">
            <xsl:number select="ancestor::contrib-group/contrib"/>
        </xsl:variable>
        <contrib>
            <xsl:attribute name="id">
                <xsl:value-of select="concat($collab_id, '.', $ndx)"/>
            </xsl:attribute>
            <xsl:apply-templates select="nompers"/>
            <xsl:apply-templates select="courriel" mode="elemif">
                <xsl:with-param name="elem_name">email</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="siteweb"/>
            <xsl:apply-templates select="affiliation/alinea" mode="xref_affiliation"/>
        </contrib>
    </xsl:template>

    <xsl:template match="surtitre">
        <article-categories>
            <subj-group>
                <xsl:attribute name="subj-group-type">heading</xsl:attribute>
                <subject>
                    <xsl:value-of select="."/>
                </subject>
                <xsl:apply-templates select="../surtitre2"/>
            </subj-group>
            <xsl:apply-templates select="../surtitreparal"/>
        </article-categories>
    </xsl:template>

    <xsl:template match="surtitreparal">
        <subj-group>
            <xsl:attribute name="subj-group-type">heading</xsl:attribute>
            <xsl:attribute name="xml:lang">
                <xsl:value-of select="@lang"/>
            </xsl:attribute>
            <subject>
                <xsl:value-of select="."/>
            </subject>
            <xsl:apply-templates select="../surtitreparal2"/>
        </subj-group>
    </xsl:template>

    <xsl:template match="surtitre2">
        <subj-group>
            <xsl:attribute name="subj-group-type">heading</xsl:attribute>
            <subject>
                <xsl:value-of select="."/>
            </subject>
            <xsl:apply-templates select="../surtitre3"/>
        </subj-group>
    </xsl:template>

    <xsl:template match="surtitreparal2">
        <subj-group>
            <xsl:attribute name="subj-group-type">heading</xsl:attribute>
            <xsl:attribute name="xml:lang">
                <xsl:value-of select="@lang"/>
            </xsl:attribute>
            <subject>
                <xsl:value-of select="."/>
            </subject>
            <xsl:apply-templates select="../surtitreparal3"/>
        </subj-group>
    </xsl:template>

    <xsl:template match="surtitre3">
        <subj-group>
            <xsl:attribute name="subj-group-type">heading</xsl:attribute>
            <subject>
                <xsl:value-of select="."/>
            </subject>
        </subj-group>
    </xsl:template>

    <xsl:template match="surtitreparal3">
        <subj-group>
            <xsl:attribute name="subj-group-type">heading</xsl:attribute>
            <xsl:attribute name="xml:lang">
                <xsl:value-of select="@lang"/>
            </xsl:attribute>
            <subject>
                <xsl:value-of select="."/>
            </subject>
        </subj-group>
    </xsl:template>

    <xsl:template match="grtitre">
        <xsl:if test="titre | sstitre">
            <title-group>
                <article-title>
                    <xsl:attribute name="xml:lang">
                        <xsl:value-of select="$document_language"/>
                    </xsl:attribute>
                    <xsl:apply-templates select="titre" mode="text_with_formating"/>
                </article-title>
                <xsl:apply-templates select="sstitre"/>
                <!-- The following apply templates retrieve a JATS structure -->
                <xsl:apply-templates select="converter:extract-trans-title-groups(., $document_language)" mode="jats_from_function"/>
            </title-group>
        </xsl:if>
    </xsl:template>

    <xsl:template match="trefbiblio">
        <product>
            <related-object><xsl:apply-templates select="." mode="text_with_formating"/></related-object>
        </product>
    </xsl:template>

    <xsl:template match="trans-title-group" mode="jats_from_function">
        <!-- This template deal with a JATS structure retrieve from the registered function trans-title-groups -->
        <trans-title-group>
            <xsl:attribute name="xml:lang">
                <xsl:value-of select="@xml:lang"/>
            </xsl:attribute>
            <xsl:apply-templates select="*" mode="jats_from_function"/>
        </trans-title-group>
    </xsl:template>

    <xsl:template match="trans-title|trans-subtitle" mode="jats_from_function">
        <!-- This template deal with a JATS structure retrieve from the registered function trans-title-groups -->
        <xsl:element name="{name()}">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="sstitre">
        <subtitle>
            <xsl:attribute name="xml:lang">
                <xsl:value-of select="$document_language"/>
            </xsl:attribute>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </subtitle>
    </xsl:template>

    <xsl:template match="idpublic" mode="article">
        <xsl:variable name="scheme">
            <xsl:value-of select="@scheme"/>
        </xsl:variable>
        <xsl:if
            test="$restriction_tab/restriction_tab/group[@value = 'article-id']/key[. = $scheme]">
            <article-id>
                <xsl:attribute name="pub-id-type">
                    <xsl:value-of select="$scheme"/>
                </xsl:attribute>
                <xsl:value-of select="."/>
            </article-id>
        </xsl:if>
    </xsl:template>

    <xsl:template match="idpublic" mode="references">
        <xsl:variable name="scheme">
            <xsl:value-of select="@scheme"/>
        </xsl:variable>
        <xsl:if
            test="$restriction_tab/restriction_tab/group[@value = 'article-id']/key[. = $scheme]">
            <pub-id>
                <xsl:attribute name="pub-id-type">
                    <xsl:value-of select="$scheme"/>
                </xsl:attribute>
                <xsl:value-of select="."/>
            </pub-id>
        </xsl:if>
    </xsl:template>

    <xsl:template match="idissnnum | idissn">
        <xsl:variable name="pub-type">
            <xsl:choose>
                <xsl:when test="name() = 'idissnnum'">epub</xsl:when>
                <xsl:otherwise>ppub</xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <issn>
            <xsl:attribute name="pub-type">
                <xsl:value-of select="$pub-type"/>
            </xsl:attribute>
            <xsl:value-of select="."/>
        </issn>
    </xsl:template>

    <xsl:template match="@id" mode="revue-id-erudit">
        <journal-id journal-id-type="publisher-id">
            <xsl:value-of select="."/>
        </journal-id>
    </xsl:template>

    <xsl:template match="titrerevabr">
        <abbrev-journal-title>
            <xsl:value-of select="."/>
        </abbrev-journal-title>
    </xsl:template>

    <xsl:template match="sstitrerev">
        <journal-subtitle>
            <xsl:value-of select="."/>
        </journal-subtitle>
    </xsl:template>

    <xsl:template match="* | text()" mode="text_with_formating">
        <xsl:apply-templates select="* | text()"/>
    </xsl:template>

    <xsl:template match="marquage[@typemarq = 'italique']">
        <italic>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </italic>
    </xsl:template>

    <xsl:template match="marquage[@typemarq = 'petitecap']">
        <sc>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </sc>
    </xsl:template>

    <xsl:template match="marquage[@typemarq = 'gras']">
        <bold>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </bold>
    </xsl:template>

    <xsl:template match="marquage[@typemarq = 'souligne']">
        <underline>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </underline>
    </xsl:template>

    <xsl:template match="marquage[@typemarq = 'surlignage']">
        <overline>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </overline>
    </xsl:template>

    <xsl:template match="marquage[@typemarq = 'filet']">
        <styled-content style-type="text-boxed">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </styled-content>
    </xsl:template>

    <xsl:template match="marquage[@typemarq = 'taillep']">
        <styled-content style-type="text-smaller">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </styled-content>
    </xsl:template>

    <xsl:template match="marquage[@typemarq = 'tailleg']">
        <styled-content style-type="text-bigger">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </styled-content>
    </xsl:template>

    <xsl:template match="marquage[@typemarq = 'barre']">
        <strike>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </strike>
    </xsl:template>
    
    <xsl:template match="marquage[@typemarq = 'majuscule']">
        <styled-content style-type="text-uppercase">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </styled-content>
    </xsl:template>

    <xsl:template match="marquage[@typemarq = 'filet']">
        <styled-content style-type="text-boxed">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </styled-content>
    </xsl:template>
    
    <xsl:template match="marquage[@typemarq = 'espacefixe']">
        <monospace>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </monospace>
    </xsl:template>
 
    <xsl:template match="exposant">
        <sup>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </sup>
    </xsl:template>

    <xsl:template match="indice">
        <sub>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </sub>
    </xsl:template>

    <xsl:template match="renvoi">
        <xref ref-type="fn" rid="fn3">
            <xsl:attribute name="ref-type">
                <xsl:call-template name="reference_tab">
                    <xsl:with-param name="group">ref-type</xsl:with-param>
                    <xsl:with-param name="key">
                        <xsl:value-of select="@typeref"/>
                    </xsl:with-param>
                </xsl:call-template>
            </xsl:attribute>
            <xsl:attribute name="rid">
                <xsl:value-of select="@idref"/>
            </xsl:attribute>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </xref>
    </xsl:template>

    <xsl:template match="liensimple">
        <ext-link>
            <xsl:attribute name="xlink:href">
                <xsl:value-of select="@xlink:href"/>
            </xsl:attribute>
            <xsl:value-of select="."/>
        </ext-link>
    </xsl:template>

    <xsl:template match="espacev">
        <break/>
    </xsl:template>

    <xsl:template match="espaceh"> </xsl:template>

    <xsl:template match="idpublic"/>

    <xsl:template match="bloccitation">
        <disp-quote>
            <xsl:attribute name="content-type">block-citation</xsl:attribute>
            <xsl:apply-templates select="*" mode="bloccitation"/>
        </disp-quote>
    </xsl:template>
    
    <xsl:template match="*" mode="bloccitation">
        <xsl:choose>
            <xsl:when test="name(.) = 'alinea'">
                <xsl:apply-templates select="." mode="paragraph"/>    
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="."/>    
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="dedicace">
        <disp-quote>
            <xsl:attribute name="content-type">dedication</xsl:attribute>
            <xsl:apply-templates select="titre"/>
            <xsl:apply-templates select="alinea" mode="paragraph"/>
            <xsl:apply-templates select="source"/>
        </disp-quote>
    </xsl:template>

    <xsl:template match="epigraphe">
        <disp-quote>
            <xsl:attribute name="content-type">epigraph</xsl:attribute>
            <xsl:apply-templates select="titre"/>
            <xsl:apply-templates select="bloccitation"/>
            <xsl:apply-templates select="alinea" mode="paragraph"/>
            <xsl:apply-templates select="source"/>
        </disp-quote>
    </xsl:template>

    <xsl:template match="grexemple">
        <boxed-text>
            <xsl:attribute name="content-type">example-group</xsl:attribute>
            <xsl:apply-templates select="*"/>
        </boxed-text>
    </xsl:template>

    <xsl:template match="exemple">
        <disp-quote>
            <xsl:attribute name="content-type">example</xsl:attribute>
            <xsl:apply-templates select="*"/>
        </disp-quote>
    </xsl:template>

    <xsl:template match="verbatim">
        <disp-quote>
            <xsl:attribute name="content-type">verbatim</xsl:attribute>
            <xsl:apply-templates select="titre"/>
            <xsl:apply-templates select="bloc/ligne"/>
            <xsl:apply-templates select="source"/>
        </disp-quote>
    </xsl:template>

    <xsl:template match="encadre">
        <boxed-text>
            <xsl:attribute name="content-type">frame</xsl:attribute>
            <xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
            <xsl:apply-templates select="*"/>
        </boxed-text>
    </xsl:template>

    <xsl:template match="encadre/section1/alinea|encadre/section1/section2/alinea|encadre/section1/section2/section3/alinea|encadre/section1/section2/section3/section4/alinea|encadre/section1/section2/section3/section4/section5/alinea|encadre/section1/section2/section3/section4/section5/section6/alinea">
        <p>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </p>
    </xsl:template>

    <xsl:template match="ligne">
        <p>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </p>
    </xsl:template>

    <xsl:template match="grequation">
        <disp-formula-group>
            <xsl:apply-templates select="no" mode="elemif">
                <xsl:with-param name="elem_name">label</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="legende"/>
            <xsl:apply-templates select="equation"/>
            <xsl:apply-templates select="notetabl"/>
            <xsl:apply-templates select="objetmedia"/>
        </disp-formula-group>
    </xsl:template>

    <xsl:template match="equation">
        <disp-formula>
            <xsl:attribute name="id">
                <xsl:value-of select="@id"/>
            </xsl:attribute>
            <xsl:apply-templates select="alinea" mode="disp-formula"/>
            <xsl:apply-templates select="no" mode="disp-formula"/>
            <xsl:apply-templates select="objetmedia | alinea/objetmedia | mml:math"/>
        </disp-formula>
    </xsl:template>

    <xsl:template match="mml:math">
        <xsl:copy-of select="."/>
    </xsl:template>

    <xsl:template match="equationligne">
        <inline-formula>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </inline-formula>    
    </xsl:template>

    <xsl:template match="alinea" mode="disp-formula">
        <xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="no" mode="disp-formula">
        <label>
            <xsl:value-of select="."/>
        </label>
    </xsl:template>

    <xsl:template match="grtableau">
        <table-wrap-group>
            <xsl:apply-templates select="no" mode="elemif">
                <xsl:with-param name="elem_name">label</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="legende"/>
            <xsl:apply-templates select="tableau"/>
            <xsl:apply-templates select="objetmedia"/>
            <!-- JATS don't support table notes in the table-wrap-group -->
        </table-wrap-group>
    </xsl:template>

    <xsl:template match="tableau">
        <table-wrap>
            <xsl:attribute name="id">
                <xsl:value-of select="@id"/>
            </xsl:attribute>
            <xsl:apply-templates select="no" mode="elemif">
                <xsl:with-param name="elem_name">label</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="legende"/>
            <xsl:apply-templates select="objetmedia | alinea/objetmedia | tabtexte"/>
            <xsl:if test="notetabl | source">
                <table-wrap-foot>
                    <xsl:apply-templates select="source"/>
                    <xsl:if test="notetabl">
                        <fn-group>
                            <xsl:apply-templates select="notetabl"/>
                        </fn-group>
                    </xsl:if>
                </table-wrap-foot>
            </xsl:if>
        </table-wrap>
    </xsl:template>


    <xsl:template match="grfigure">
        <fig-group>
            <xsl:apply-templates select="no" mode="elemif">
                <xsl:with-param name="elem_name">label</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="legende"/>
            <xsl:apply-templates select="figure"/>
            <xsl:apply-templates select="notefig"/>
            <xsl:apply-templates select="objetmedia"/>
        </fig-group>
    </xsl:template>

    <xsl:template match="figure">
        <fig>
            <xsl:attribute name="id">
                <xsl:value-of select="@id"/>
            </xsl:attribute>
            <xsl:apply-templates select="no" mode="elemif">
                <xsl:with-param name="elem_name">label</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="legende"/>
            <xsl:apply-templates select="notefig"/>
            <xsl:apply-templates select="objetmedia"/>
            <xsl:apply-templates select="source"/>
        </fig>
    </xsl:template>
    
    <xsl:template match="objet">
        <media>
            <xsl:if test="objetmedia/video">
               <xsl:attribute name="mimetype">video</xsl:attribute>
                <xsl:apply-templates select="objetmedia/video/@id" mode="attrif">
                    <xsl:with-param name="attr-name">id</xsl:with-param>
                </xsl:apply-templates>
               <xsl:apply-templates select="objetmedia/video/@typemime" mode="attrif">
                   <xsl:with-param name="attr_name">mime-subtype</xsl:with-param>
               </xsl:apply-templates>
               <xsl:apply-templates select="objetmedia/video/@xlink:href" mode="attrif">
                   <xsl:with-param name="attr_name">xlink:href</xsl:with-param>
               </xsl:apply-templates>
               <xsl:apply-templates select="objetmedia/video/@xlink:show" mode="attrif">
                   <xsl:with-param name="attr_name">xlink:show</xsl:with-param>
               </xsl:apply-templates>
                <xsl:apply-templates select="objetmedia/video/@xlink:actuate" mode="attrif">
                   <xsl:with-param name="attr_name">xlink:actuate</xsl:with-param>
               </xsl:apply-templates>
               <xsl:apply-templates select="objetmedia/video/@xlink:type" mode="attrif"/>
               <xsl:apply-templates select="no" mode="elemif">
                   <xsl:with-param name="elem_name">label</xsl:with-param>
               </xsl:apply-templates>
            </xsl:if>
            <xsl:if test="objetmedia/audio">
                <xsl:attribute name="mimetype">audio</xsl:attribute>
                <xsl:apply-templates select="objetmedia/audio/@id" mode="attrif">
                    <xsl:with-param name="attr-name">id</xsl:with-param>
                </xsl:apply-templates>
                <xsl:apply-templates select="objetmedia/audio/@typemime" mode="attrif">
                    <xsl:with-param name="attr_name">mime-subtype</xsl:with-param>
                </xsl:apply-templates>
                <xsl:apply-templates select="objetmedia/audio/@xlink:href" mode="attrif">
                    <xsl:with-param name="attr_name">xlink:href</xsl:with-param>
                </xsl:apply-templates>
                <xsl:apply-templates select="objetmedia/audio/@xlink:show" mode="attrif">
                    <xsl:with-param name="attr_name">xlink:show</xsl:with-param>
                </xsl:apply-templates>
                <xsl:apply-templates select="objetmedia/audio/@xlink:actuate" mode="attrif">
                    <xsl:with-param name="attr_name">xlink:actuate</xsl:with-param>
                </xsl:apply-templates>
                <xsl:apply-templates select="objetmedia/audio/@xlink:type" mode="attrif"/>
                <xsl:apply-templates select="no" mode="elemif">
                    <xsl:with-param name="elem_name">label</xsl:with-param>
                </xsl:apply-templates>
            </xsl:if>
            <xsl:apply-templates select="legende"/>
            <xsl:apply-templates select="noteobjet"/>
            <xsl:apply-templates select="source"/>
        </media>
    </xsl:template>

    <xsl:template match="legende">
        <caption>
            <xsl:apply-templates select="@lang" mode="attrif">
                <xsl:with-param name="attr_name">xml:lang</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="titre"/>
            <xsl:apply-templates select="alinea" mode="paragraph"/>
        </caption>
    </xsl:template>

    <xsl:template match="notefig | noteeq | noteobjet">
        <alt-text>
            <xsl:apply-templates select="@lang" mode="attrif">
                <xsl:with-param name="attr_name">xml:lang</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </alt-text>
    </xsl:template>

    <xsl:template match="notetabl">
        <fn>
            <xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
            <xsl:apply-templates select="@lang" mode="attrif">
                <xsl:with-param name="attr_name">xml:lang</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="no"/>
            <xsl:apply-templates select="alinea" mode="paragraph"/>
        </fn>
    </xsl:template>

    <xsl:template match="source">
        <attrib>
            <xsl:apply-templates select="@lang" mode="attrif">
                <xsl:with-param name="attr_name">xml:lang</xsl:with-param>
            </xsl:apply-templates>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </attrib>
    </xsl:template>
 
    <xsl:template match="objetmedia">
        <graphic>
            <xsl:if test="image/@id">
                <xsl:attribute name="id"><xsl:value-of select="image/@id"/></xsl:attribute>
            </xsl:if>
            <xsl:choose>
                <xsl:when test="image/@xlink:href">
                    <xsl:attribute name="xlink:href">
                        <xsl:value-of select="image/@xlink:href"/>
                    </xsl:attribute>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:attribute name="xlink:href">
                        <xsl:value-of select="image/@id"/>
                    </xsl:attribute>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:attribute name="position">
                <xsl:call-template name="reference_tab">
                    <xsl:with-param name="group">image-position</xsl:with-param>
                    <xsl:with-param name="key">
                        <xsl:value-of select="@flot"/>
                    </xsl:with-param>
                </xsl:call-template>
            </xsl:attribute>
            <xsl:attribute name="content-type">
                <xsl:call-template name="reference_tab">
                    <xsl:with-param name="group">image-type</xsl:with-param>
                    <xsl:with-param name="key">
                        <xsl:value-of select="image/@typeimage"/>
                    </xsl:with-param>
                </xsl:call-template>
            </xsl:attribute>
        </graphic>
    </xsl:template>
    
    <xsl:template match="objetmedia[@flot='ligne']">
        <inline-graphic>
            <xsl:choose>
                <xsl:when test="image/@xlink:href">
                    <xsl:attribute name="xlink:href">
                        <xsl:value-of select="image/@xlink:href"/>
                    </xsl:attribute>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:attribute name="xlink:href">
                        <xsl:value-of select="image/@id"/>
                    </xsl:attribute>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:attribute name="content-type">
                <xsl:call-template name="reference_tab">
                    <xsl:with-param name="group">image-type</xsl:with-param>
                    <xsl:with-param name="key">
                        <xsl:value-of select="image/@typeimage"/>
                    </xsl:with-param>
                </xsl:call-template>
            </xsl:attribute>
        </inline-graphic>
    </xsl:template>

    <xsl:template match="tabtexte">
        <table>
            <xsl:apply-templates select="tabgrcol"/>
            <xsl:apply-templates select="tabentete"/>
            <xsl:apply-templates select="tabpied"/>
            <xsl:apply-templates select="tabgrligne"/>
        </table>
    </xsl:template>

    <xsl:template match="tabgrcol">
        <colgroup>
            <xsl:apply-templates select="tabcol"/>
        </colgroup>
    </xsl:template>
    
    <xsl:template match="tabcol">
            <col>
                <xsl:if test="@alignh">
                    <xsl:attribute name="align">
                        <xsl:call-template name="reference_tab">
                            <xsl:with-param name="group">table-cel-halign</xsl:with-param>
                            <xsl:with-param name="key">
                                <xsl:value-of select="@alignh"/>
                            </xsl:with-param>
                        </xsl:call-template>
                    </xsl:attribute>
                </xsl:if>
                <xsl:if test="@alignv">
                    <xsl:attribute name="valign">
                        <xsl:call-template name="reference_tab">
                            <xsl:with-param name="group">table-cel-valign</xsl:with-param>
                            <xsl:with-param name="key">
                                <xsl:value-of select="@alignv"/>
                            </xsl:with-param>
                        </xsl:call-template>
                    </xsl:attribute>
                </xsl:if>
                <xsl:if test="@carac">
                    <xsl:attribute name="char"><xsl:value-of select="@carac"/></xsl:attribute>
                </xsl:if>
                <xsl:if test="@nbcol">
                    <xsl:attribute name="span"><xsl:value-of select="@nbcol"/></xsl:attribute>
                </xsl:if>
                <xsl:value-of select="."/>
            </col>
    </xsl:template>

    <xsl:template match="tabentete">
        <thead>
            <xsl:apply-templates select="*">
                <xsl:with-param name="style">th</xsl:with-param>
            </xsl:apply-templates>
        </thead>
    </xsl:template>

    <xsl:template match="tabgrligne">
        <tbody>
            <xsl:apply-templates select="*">
                <xsl:with-param name="style">td</xsl:with-param>
            </xsl:apply-templates>
        </tbody>
    </xsl:template>

    <xsl:template match="tabpied">
        <tfoot>
            <xsl:apply-templates select="*">
                <xsl:with-param name="style">td</xsl:with-param>
            </xsl:apply-templates>
        </tfoot>
    </xsl:template>

    <xsl:template match="tabligne">
        <xsl:param name="style"/>
        <tr>
            <xsl:apply-templates select="tabcellulee | tabcelluled">
                <xsl:with-param name="style">
                    <xsl:value-of select="$style"/>
                </xsl:with-param>
            </xsl:apply-templates>
        </tr>
    </xsl:template>

    <xsl:template match="tabcellulee | tabcelluled">
        <xsl:param name="style"/>
        <xsl:variable name="pos" select="position()"/>
        <xsl:variable name="general-halign"
            select="../../../tabgrcol//tabcol[position() = $pos]/@alignh"/>
        <xsl:variable name="general-valign"
            select="../../../tabgrcol//tabcol[position() = $pos]/@alignv"/>
        <xsl:element name="{$style}">
            <xsl:if test="@alignh">
                <xsl:attribute name="align">
                    <xsl:call-template name="reference_tab">
                        <xsl:with-param name="group">table-cel-halign</xsl:with-param>
                        <xsl:with-param name="key">
                            <xsl:value-of select="@alignh"/>
                        </xsl:with-param>
                    </xsl:call-template>
                </xsl:attribute>
            </xsl:if>
            <xsl:if test="@alignv">
                <xsl:attribute name="valign">
                    <xsl:call-template name="reference_tab">
                        <xsl:with-param name="group">table-cel-valign</xsl:with-param>
                        <xsl:with-param name="key">
                            <xsl:value-of select="@alignv"/>
                        </xsl:with-param>
                    </xsl:call-template>
                </xsl:attribute>
            </xsl:if>
            <xsl:if test="@carac">
                <xsl:attribute name="char"><xsl:value-of select="@carac"/></xsl:attribute>
            </xsl:if>
            <xsl:if test="@nbligne">
                <xsl:attribute name="rowspan"><xsl:value-of select="@nbligne"/></xsl:attribute>
            </xsl:if>
            <xsl:if test="@nbcol">
                <xsl:attribute name="colspan"><xsl:value-of select="@nbcol"/></xsl:attribute>
            </xsl:if>
            <xsl:if test="@alignh != '' or $general-halign != ''">
                <xsl:attribute name="align">
                    <xsl:choose>
                        <xsl:when test="@alignh">
                            <xsl:call-template name="reference_tab">
                                <xsl:with-param name="group">table-cel-halign</xsl:with-param>
                                <xsl:with-param name="key">
                                    <xsl:value-of select="@alignh"/>
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

            <xsl:if test="@alignv != '' or $general-valign != ''">
                <xsl:attribute name="valign">
                    <xsl:choose>
                        <xsl:when test="@alignv">
                            <xsl:call-template name="reference_tab">
                                <xsl:with-param name="group">table-cel-valign</xsl:with-param>
                                <xsl:with-param name="key">
                                    <xsl:value-of select="@alignv"/>
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
            <xsl:apply-templates select="alinea" mode="alinea-table"/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="alinea" mode="alinea-table">
        <xsl:apply-templates select="." mode="text_with_formating"/>
    </xsl:template>

    <xsl:template match="listerelation">
        <def-list>
            <xsl:attribute name="list-content"><xsl:value-of select="@type"/></xsl:attribute>
            <xsl:if test="lrsourcee">
                <term-head>
                    <xsl:apply-templates select="lrsourcee"/>
                </term-head>
            </xsl:if>
            <xsl:if test="lrciblee">
                <def-head>
                    <xsl:apply-templates select="lrciblee"/>
                </def-head>
            </xsl:if>
            <xsl:apply-templates select="elemrelation"/>
        </def-list>
    </xsl:template>

    <xsl:template match="elemrelation">
        <def-item>
            <xsl:apply-templates select="*"/>
        </def-item>
    </xsl:template>

    <xsl:template match="lrsourcee">
        <xsl:value-of select="*"/>
    </xsl:template>

    <xsl:template match="lrciblee">
        <xsl:value-of select="*"/>
    </xsl:template>

    <xsl:template match="lrsource">
        <term>
            <xsl:apply-templates select="*"/>
        </term>

    </xsl:template>

    <xsl:template match="lrcible">
        <def>
            <xsl:apply-templates select="*"/>
        </def>
    </xsl:template>

    <xsl:template match="listeord">
        <list>
            <xsl:attribute name="list-type">order</xsl:attribute>
            <xsl:apply-templates select="elemliste"/>
        </list>
    </xsl:template>

    <xsl:template match="listenonord">
        <list>
            <xsl:attribute name="list-type">simple</xsl:attribute>
            <xsl:apply-templates select="elemliste"/>
        </list>
    </xsl:template>

    <xsl:template match="elemliste">
        <list-item>
            <xsl:apply-templates select="*"/>
        </list-item>
    </xsl:template>

    <xsl:template match="texte">
        <p><xsl:value-of select="."/></p>
    </xsl:template>

    <xsl:template match="* | @*">
        <PENDING-TREATMENT>
            <xsl:copy-of select="."/>
        </PENDING-TREATMENT>
    </xsl:template>

</xsl:stylesheet>
