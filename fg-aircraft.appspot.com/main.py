# -*- coding: utf-8 -*-
import os
import cgi

from google.appengine.api import users

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext import db


import app.Index
import app.PilotsOnline

application = webapp.WSGIApplication([	('/', app.Index.Index),
										('/pilots_online', app.PilotsOnline.PilotsOnline)
									],
									debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()