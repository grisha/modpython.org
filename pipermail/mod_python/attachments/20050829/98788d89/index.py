from mod_python import apache,psp

def index(req):
    quote = 'quote_of_the_day'
    tmpl = psp.PSP(req, filename='templates/index.tmpl')
    tmpl.run( vars={'QUOTES':quote} )
    return apache.OK
    