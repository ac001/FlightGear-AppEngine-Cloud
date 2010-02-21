# -*- coding: utf-8 -*-
import os
import cgi

from google.appengine.api import users

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext import db



class Index(webapp.RequestHandler):


	
	def get(self):



		template_values = {

			}
		#print template_values
		path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
		self.response.out.write(template.render(path, template_values))
		
