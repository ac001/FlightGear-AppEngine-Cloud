# -*- coding: utf-8 -*-

import os
import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


import app.Handler
# 										('/cron/pilots_online', app.PilotsOnline.PilotsOnl
application = webapp.WSGIApplication([	
										('/(.*)/(.*)/', app.Handler.HandlerPage),
										('/(.*)/', app.Handler.HandlerPage),
										('/', app.Handler.HandlerPage),
										
									],
									debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()