#!/usr/bin/env python

'''
Summarize the NXDL classes definitions for the given NXDL section.

Re-write the index.rst file with a list of: class  summary (and a hidden toctree)
'''


import os, sys
import lxml.etree


TITLE_MARKERS = '- + ~ ^ * @'.split()  # used for underscoring section titles
INDENTATION = ' '*4


NAMESPACE = 'http://definition.nexusformat.org/nxdl/3.1'
NS = {'nx': NAMESPACE}


PREAMBLES = {
    'base_classes': '''
.. index::
     ! see: class definitions; base class
     ! base class

.. _base.class.definitions:

Base Class Definitions
######################

A description of each NeXus base class definition is given.
NeXus base class definitions define the set of terms that
*might* be used in an instance of that class.
Consider the base classes as a set of *components*
that are used to construct a data file.
    ''',

    'applications': '''
    ''',
    
    'contributed_definitions': '''
    ''',
}


def getSummary(nxdl_file):
    '''
    get the summary line from each NXDL definition doc
    
    That's the first physical line of the doc string.
    '''
    tree = lxml.etree.parse(nxdl_file)
    root = tree.getroot()
    nodes = root.xpath('nx:doc', namespaces=NS)
    if len(nodes) != 1:
        raise RuntimeError('wrong number of <doc> nodes in NXDL: ' + nxdl_file)
    text = nodes[0].text
    return text.strip().splitlines()[0]


def command_args():
    '''get the command-line arguments, handle syntax errors'''
    import argparse
    doc = __doc__.strip().splitlines()[0]
    parser = argparse.ArgumentParser(prog=sys.argv[0], description=doc)
    parser.add_argument('section',
                        action='store', 
                        help="NXDL section (such as *base_classes*)")
    return parser.parse_args()


def main(section):
    if section not in PREAMBLES.keys():
        raise KeyError('unknown NXDL section: ' + section)
    base_path = os.path.abspath(os.path.dirname(__file__))
    nxdl_path = os.path.abspath(os.path.join(base_path, '..', section))
    if not os.path.exists(nxdl_path):
        raise IOError('not found: ' + nxdl_path)

    rst_path = os.path.abspath(os.path.join(base_path, '..', 'manual', 'source', 'classes', section))
    if not os.path.exists(rst_path):
        raise IOError('not found: ' + rst_path)

    index_file = os.path.join(rst_path, 'index.rst')

    classes = []
    text = []
    text.append('''
.. do NOT edit this file
   automatically generated by script ''' + __file__)
    text.append('')
    text.append(PREAMBLES[section])
    for fname in sorted(os.listdir(nxdl_path)):
        if fname.endswith('.nxdl.xml'):
            class_name = fname.split('.')[0]
            classes.append(class_name)
            summary = getSummary(os.path.join(nxdl_path, fname))
            text.append('')
            text.append(':ref:`' + class_name + '`')
            text.append(INDENTATION + summary)
    text.append('')
    text.append('.. toctree::')
    text.append(INDENTATION + ':hidden:')
    text.append('')
    for cname in sorted(classes):
        text.append(INDENTATION + cname)
    text.append('')
    open(index_file, 'w').writelines('\n'.join(text))


if __name__ == '__main__':
    cli = command_args()
    main(cli.section)
