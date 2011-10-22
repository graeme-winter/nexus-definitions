#!/usr/bin/env python
"""
   Generate the DocBook header for the 
   NeXus manual section identified in sys.argv[1]
   Section classes are supplied in sys.argv[2:]
"""

########### SVN repository information ###################
# $Date: 2008$
# $Author$
# $Revision$
# $HeadURL$
# $Id$
########### SVN repository information ###################

import sys

category = sys.argv[1]
classes = sys.argv[2:]

xref = {
    'base': "base classes",
    'application': "application definitions",
    'contributed': "contributed definitions"
}
secondary = xref[category.lower()]

explanation = {
   'base': 
        '''
            <!--Note for editors: 
				This paragraph is created in the Python source code-->
			A description of each NeXus base class definition is given.
            NeXus base class definitions define the <emphasis>complete</emphasis>
            set of terms that
            <emphasis>might</emphasis> be used in an instance of that class.
            Consider the base classes as a set of <emphasis>components</emphasis>
            that are used to construct a data file.
        ''',
   'application': 
        '''
            <!--Note for editors: 
				This paragraph is created in the Python source code-->
            A description of each NeXus application definition is given.
            NeXus application definitions define the <emphasis>minimum</emphasis>
            set of terms that
            <emphasis>must</emphasis> be used in an instance of that class.
            Consider the application definitions as a <emphasis>contract</emphasis>
            between a data provider (such as the beamline control system) and a 
            data consumer (such as a data analysis program for a scientific technique)
            that describes the information is certain to be available in a data file.
        ''',
   'contributed': 
        '''
            <!--Note for editors: 
				This paragraph is created in the Python source code-->
            A description of each NeXus contributed definition is given.
            NXDL files in the NeXus contributed definitions include propositions from
            the community for NeXus base classes or application definitions, as well
            as other NXDL files for long-term archival by NeXus.  Consider the contributed
            definitions as either in <emphasis>incubation</emphasis> or a special
            case not for general use.  The NIAC is charged to review any new contributed 
            definitions and provide feedback to the authors before ratification
            and acceptance as either a base class or application definition.
        '''
}

print '<?xml version="1.0" encoding="UTF-8"?>'
print '<?oxygen RNGSchema="http://www.oasis-open.org/docbook/xml/5.0/rng/docbook.rng" type="xml"?>'
print '<!-- autogenerated from the Makefile, do NOT edit this file, do NOT put in version control -->'
print '<!-- written by: $Id$ -->'
print '<section xml:id="ClassDefinitions-%s" version="5.0" xmlns="http://docbook.org/ns/docbook" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xi="http://www.w3.org/2001/XInclude">' % category
print '  <title>NeXus %s Classes</title>' % category
print '  <indexterm significance="preferred"><primary>classes</primary><secondary>%s</secondary></indexterm>' % secondary
print '  <para>%s</para>' % explanation[category.lower()]
if len(classes) == 0:
	print '  <para>No NeXus %s Classes were defined as this version of the manual was created.</para>' % category
else:
    print "  <para>"
    print "    <itemizedlist>"
    for item in classes:
        cl = item.split("/")[1].split(".")[0]
        href = '<link xlink:href="#%s">%s</link>' % (cl, cl)
        print '      <listitem><para>%s</para></listitem>' % href
    print "    </itemizedlist>"
    print "  </para>"
    for item in classes:
    	cl = item.split("/")[1]
    	print '  <xi:include href="%s" />' % cl
print '</section>'

