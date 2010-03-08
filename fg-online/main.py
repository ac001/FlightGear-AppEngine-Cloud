# -*- coding: utf-8 -*-


from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


import app.Handler
import app.Import

application = webapp.WSGIApplication([	
										#('/(.*)/(.*)/', app.Handler.HandlerPage),
										('/update/', app.Handler.UpdateStatus),
										('/import/', app.Import.ImportHandler),
										('/rpc/', app.Handler.RPCHandler),
										('/(.*)/', app.Handler.HandlerPage),
										('/', app.Handler.HandlerPage),
										
									],
									debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()