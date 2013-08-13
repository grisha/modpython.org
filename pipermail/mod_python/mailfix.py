
from mod_python import apache, util
import os

def handler(req):

    if not os.path.exists(req.filename):

        fpath, fname = os.path.split(req.filename)
        fname, fext = os.path.splitext(fname)

        try:
            n = int(fname)
            n = n+10527
            if n < 20000:
                util.redirect(req, '%06d.html' % n, permanent=1)
        except:
            pass

    # default
    return apache.DECLINED
