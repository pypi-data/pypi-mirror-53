# mPyPl - Monadic Pipeline Library for Python
# http://github.com/shwars/mPyPl

import os
import xml.etree.ElementTree as et
from .mdict import *

def populate_mdict_from_xml(xml,m, prefix='',list_fields=[],flatten_fields=[],skip_fields=[]):
    """
    Construct `mdict` object from part of XML tree
    :param xml: part of `ElementTree` XML DOM
    :param prefix: prefix to use for each field (useful for recursive calls)
    :param list_fields: fields to be treated as lists (useful is we know that certain values will be present more than once)
    :param flatten_fields: fields to be flattened
    :param skip_fields: fields to be skipped
    :return: mdict object
    """
    def addf(md,n,x): # add field n with value x, handle situations when value already exists
        n = prefix+n
        if n in md.keys():
            if isinstance(md[n],list):
                md[n].append(x)
            else:
                md[n] = [md[n],x]
        else:
            md[n] = [x] if n in list_fields else x
    for x in xml:
        if x.tag in skip_fields:
            continue
        if len(x)==0: # atomic value
            addf(m,x.tag,x.text)
        else:
            if x.tag in flatten_fields:
                populate_mdict_from_xml(x,m,prefix+x.tag+"_",list_fields,flatten_fields)
            else:
                m1 = mdict()
                populate_mdict_from_xml(x,m1,'',list_fields,flatten_fields)
                addf(m,x.tag,m1)

def get_xmlstream_from_dir(dir,ext='.xml',list_fields=[],flatten_fields=[],skip_fields=[],populate_aux_fields=False):
    """
    Returns the stream of XML objects retrieved from files in the given directory. This can be used, for example, for
    reading Pascal VOC annotations.
    :param dir: Directory of XML files to use
    :param list_fields: fields to be treated as lists (useful is we know that certain values will be present more than once)
    :param flatten_fields: fields to be flattened
    :param skip_fields: fields to be skipped
    :return: A stream of `mdict`s with fields corresponding to XML elements
    """
    for f in os.listdir(dir):
        if ext is not None and not f.endswith(ext):
            continue
        doc = et.parse(os.path.join(dir,f))
        m = mdict()
        if populate_aux_fields:
            m['__original_filename__'] = f
            m['__original_filepath__'] = os.path.join(dir,f)
        populate_mdict_from_xml(doc.getroot(),m,'',list_fields,flatten_fields)
        yield m

def get_pascal_annotations(dir='Annotations',ext='.xml',skip_fields=[]):
    """
    Return stream of bounding box annotations from Pascal VOC annotation directory
    :param dir: Directory where XML files with annotations are, defaults to 'Annotations'
    :param ext: Extension, defaults to '.xml'
    :param skip_fields: Fields to skip
    :return: Datastream
    """
    return get_xmlstream_from_dir(dir,list_fields=['object'],flatten_fields=['bndbox','size'],skip_fields=skip_fields+['pose','source','path'])
