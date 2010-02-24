# -*- coding: utf-8 -*-
import os
import cgi

from google.appengine.api import users

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app


import conf
import app.fetch

class Index(webapp.RequestHandler):


	def get(self):
	
		template_values = {
			'title': 'Welcome', 'conf': conf, 'path': self.request.path,
			'servers': app.fetch.mpservers()
			}
		path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
		self.response.out.write(template.render(path, template_values))
		
