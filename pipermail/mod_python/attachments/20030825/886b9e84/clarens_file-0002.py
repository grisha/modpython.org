#    Clarens file utilities
#
#    Copyright (C) 2003 California Institute of Technology
#    Author: Conrad D. Steenberg <conrad@hep.caltech.edu>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or   
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of 
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the  
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import sys
import os
import mmap
import time
import re
import string
class dummy:
  OK=200
  HTTP_BAD_REQUEST=400
  def __init__(self):
    pass

try:
  from mod_python import apache
except:
  apache=dummy()
  print apache.OK

import xmlrpc
import clarens_util
import stat
import fnmatch
import mimetypes

typemap=None

def init_typemap(req):
  global typemap
  options=req.get_options()
  typemap=mimetypes.read_mime_types(options['clarens_path']+"/mime.types")


def send_file_slow(req,filename,offset,length,fd,size,num):
# Default size is the whole file
  headers_sent=0
  readnum=0
  oldreadnum=readnum
  try:
    while 1:
      data=os.read(fd,1024*1024)
      if not data: raise IOError
      oldreadnum=readnum
      readnum=readnum+len(data)
      if num-oldreadnum>=readnum-oldreadnum:
        req.write(data)
      elif num-oldreadnum<readnum-oldreadnum:
        req.write(data[:num-oldreadnum])
      if readnum>=num: break
  except:
    raise #OSError(5,"Error sending file")


def send_file(req,filename,offset,length):

  """read
     Arguments: filename (string)
                offset   (int)
                length   (int)
     Reads 'length' bytes from the file 'filename', starting at 'offset'"""
  global typemap
  try:
    if not typemap:
      init_typemap(req)
  except:
    raise #OSError(1,"Could not initialize MIME types")
  size=-1
  path=os.path.split(filename)
  if path[1]:
    basename=path[1]
  else:
    basename=os.path.basename(path[0])
  if basename[0]==".":
    raise OSError(2,"No such file or directory")
  try:
    status=os.stat(filename)
    fd=os.open(filename,os.O_RDONLY)
    size=status[6]
    if not stat.S_ISREG(status[0]): raise OSError(3,"Not a regular file")
    if size==-1: raise OSError(3,"Unable to stat file")
  except OSError:
    raise
  except:
    raise OSError(3,"Unable to stat file")
  
  if length==-1:
    bytes=size-offset
  else:
    bytes=length


  req.headers_out['Server']='Sourcelight Technologies py-xmlrpc-0.8.8.2'
  try:
    ext=string.split(os.path.basename(filename),'.')[1]
    req.content_type=typemap['.'+ext]
  except:
    req.content_type='text/plain'
  try:
    req.headers_out['Status'] = '200'
    req.headers_out['Content-Length']=str(bytes)
    req.send_http_header();
  except:
    raise OSError(4,"Unable to write header information")

  if not hasattr(req,"write_file"):
    return send_file_slow(req,filename,offset,length,fd,size,bytes)
  try:
    while bytes>0:
      sent=0
      sent=req.write_file(filename,offset,bytes)
      if sent<0: raise OSError(5,"Error sending file")
      offset=offset+sent
      bytes=bytes-sent
  except:
    raise OSError(5,"Error sending file")
