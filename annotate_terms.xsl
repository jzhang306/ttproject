<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="xml" indent="yes"/>

  <!-- Root element -->
  <xsl:template match="/articles">
    <articles>
      <xsl:apply-templates select="article"/>
    </articles>
  </xsl:template>

  <!-- Handle each article -->
  <xsl:template match="article">
    <article>
      <xsl:copy-of select="title"/>
      <xsl:copy-of select="author"/>
      <xsl:copy-of select="date"/>
      <xsl:copy-of select="discipline"/>
      <xsl:copy-of select="source"/>

      <!-- Keep annotated abstract and term tags -->
      <abstract>
        <xsl:apply-templates select="abstract/node()"/>
      </abstract>
    </article>
  </xsl:template>

  <!-- Copy all child nodes (including <term>) inside abstract -->
  <xsl:template match="term">
    <term>
      <xsl:apply-templates/>
    </term>
  </xsl:template>

  <!-- Pass through plain text or other elements -->
  <xsl:template match="node()|@*">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
