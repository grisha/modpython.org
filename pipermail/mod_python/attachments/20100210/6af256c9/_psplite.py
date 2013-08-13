# coding=utf-8
# ---------------------------------------------------------------
# Project: TeamPortal
# Source : _psplite.py
# Date   : Thu May 24 11:14:35 CEST 2009
# Author : TeamSystem Spa
# Contact: http://www.teamsystem.com
# License: see _libs/_licenses/
# ---------------------------------------------------------------
#
# Cache code from mod_python 3.3.1 -> psp.py :
#
# Copyright 2004 Apache Software Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License.  You
# may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.  See the License for the specific language governing
# permissions and limitations under the License.
#
# This file originally written by Sterling Hughes
#
# $Id: psp.py 472053 2006-11-07 10:11:01Z grahamd $

import os
import re

delimiter = re.compile(r"<%=(.*?)%>", re.DOTALL)

class PSP(object):
    '''
    PSP lite class
    '''

    def __init__(self,req,pspname,pspvars):
        self.req = req
        self.html = None
        self.pspvars = dict(pspvars)
        self.compile(pspname)

    def compile(self,pspname):
        if pspname.startswith('/str:'):
            # da stringa
            template = pspname[5:]
            #in cache?
            cached = mem_scache.get(template)
            if cached:
                self.code = cached
                return
        else:
            # from file
            mtime = os.path.getmtime(pspname)
            # check cache
            cached = mem_fcache.get(pspname, mtime)
            if cached:
                self.code = cached
                return
            template = file(pspname,'rb').read()

        source = ''
        for i, part in enumerate(delimiter.split(template)):
            if i % 2 == 0:
                if part:
                    source += "__write(%r);" % part
            else:
                source += "__write(str(%s));" % part.strip()
        self.code = compile(source, '<string>', 'exec')
        # store in cache
        if pspname.startswith('/str:'):
            mem_scache.store(template,self.code)
        else:
            mem_fcache.store(pspname, mtime, self.code)

    def render(self):
        if self.html is not None:
            return
        output = []
        self.pspvars["__write"] = output.append
        exec self.code in self.pspvars
        self.html = ''.join(output)
        return self.html

    def run(self):
        self.render()
        # no flush
        self.req.write(self.html,0)


class HitsCache:

    def __init__(self, size=512):
        self.cache = {}
        self.size = size

    def store(self, key, val):
        self.cache[key] = (1, val)
        if len(self.cache) > self.size:
            self.clean()

    def get(self, key):
        if key in self.cache:
            hits, val = self.cache[key]
            self.cache[key] = (hits+1, val)
            return val
        else:
            return None

    def clean(self):
        byhits = [(n[1], n[0]) for n in self.cache.items()]
        byhits.sort()

        # delete enough least hit entries to make cache 75% full
        for item in byhits[:len(self.cache)-int(self.size*.75)]:
            val, key = item
            del self.cache[key]

mem_scache = HitsCache()

class FileCache(HitsCache):

    def store(self, filename, mtime, code):
        self.cache[filename] = (1, mtime, code)
        if len(self.cache) > self.size:
            self.clean()

    def get(self, filename, mtime):
        try:
            hits, c_mtime, code = self.cache[filename]
            if mtime != c_mtime:
                del self.cache[filename]
                return None
            else:
                self.cache[filename] = (hits+1, mtime, code)
                return code
        except KeyError:
            return None

mem_fcache = FileCache()
