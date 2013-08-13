#! /usr/bin/env python

import sys, os, time, string
import HTMLgen as H
from mod_python			import apache, util


def dbg(msg):
	log = open('/tmp/jsa.log', 'a')
	log.write(msg + '\n')
	log.close()


from types import *
from mod_python.util import StringField

def patch_getitem(self, key):
	"""Dictionary style indexing."""
	if self.list is None:
		raise TypeError, "not indexable"
	found = []
	for item in self.list:
		dbg('item.name=%s' % `item.name`)
		if item.name == key:
			dbg('item=%s' % `item`)
			dbg('item.type=%s' % `item.type`)
			dbg('item.type_options=%s' % `item.type_options`)
			dbg('type(item)=%s' % `type(item)`)
			dbg('item.value=%s' % `item.value`)
			dbg('item.file.read()=%s' % `item.file.read()`)
			if isinstance(item.file, FileType) or \
				isinstance(getattr(item.file, 'file', None), FileType):
				found.append(item)
			else:
				found.append(StringField(item.value))
	if not found:
		raise KeyError, key
	if len(found) == 1:
		return found[0]
	else:
		return found

util.FieldStorage.__getitem__ = patch_getitem


def handler(req):
	dbg('-'*80)

	req.content_type = 'text/html'
	#req.content_type = 'multipart/form-data'

	# Did the user just respond to a form?
	fs = util.FieldStorage(req)
	if fs.has_key('inputJar'):
		inputJar = fs['inputJar']
		dbg('inputJar=%s' % `inputJar`)
		dbg('type(inputJar)=%s' % `type(inputJar)`)
		dbg('dir(inputJar)=%s' % `dir(inputJar)`)

	# Build a new page.
	doc = H.SeriesDocument(None, title='Products', cgi=0)
	f = H.Form(submit = H.Input(type='submit', name = 'add product',
		value='Add Product'),
		cgi = 'http://mudd.homeip.net/javaSignAuto/jsa.py')
	i = H.Input(name='inputJar', type='file')
	f.append(i)
	doc.append(f)
	req.write(str(doc))

	return apache.OK
