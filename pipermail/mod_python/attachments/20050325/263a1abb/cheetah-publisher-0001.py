from mod_python import apache
from mod_python import util

import os

# It is assumed that Apache config or .htaccess file
# blocks access to ".tmpl", ".py" and ".pyc" files.

def handler(req):

  # Assume REST style URLs. Ie., no extension is used
  # for accessing Cheetah pages. On this basis, first
  # perform a check that there is a ".py" file in
  # existance. This is done because can't distinguish
  # between a non existant module and a module which has
  # a coding error in it when using the function
  # "apache.import_module()". By returning DECLINED,
  # Apache will then serve up any static files in the
  # directory which may otherwise be matched.

  target = req.filename + ".py"

  if not os.path.exists(target):
    return apache.DECLINED

  # Grab the module name to look for from the last part
  # of the path. This means that pages can be spread
  # across subdirectories as well.

  directory,module_name = os.path.split(req.filename)

  # Import the module. Any coding error in the module
  # being imported is thrown back to the user. Error
  # also results if by chance the target just vanished.

  module = apache.import_module(module_name,[directory])

  # Ensure that there is a class defined in the module
  # of the appropriate name.
  if not hasattr(module,module_name): # This is probably a standalone
    # Python program
    if not hasattr(module, "index"):
      return apache.DECLINED
    else:
      req.content_type = "text/html"
      req.send_http_header()
      index_proc = getattr(module, "index")
      req.form = util.FieldStorage(req, keep_blank_values=1)
      result = str(index_proc(req))
      req.write(result)
      return apache.OK
  
  else: # This is a Cheetah template
    # Create instance of the class and setup request object.

    tmpl = getattr(module,module_name)()
    tmpl.req = req
    
    # Assume that HTML is being generated.

    req.content_type = "text/html"
    req.send_http_header()
    
    # Now generate the actual content and return it.
    
    req.write(tmpl.respond())
    
    return apache.OK


