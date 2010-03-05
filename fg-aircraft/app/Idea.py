# -*- coding: utf-8 -*-
import os
import cgi

#from google.appengine.api import users

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
#from google.appengine.ext.webapp.util import run_wsgi_app


import iconf
#import app.fetch

class IdeaPage(webapp.RequestHandler):


	def get(self):
	
		template_values = {
			'title': 'Welcome', 
			'path': '/idea/',
			'iconf': iconf
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/idea.html')
		self.response.out.write(template.render(path, template_values))
		



class LashUpPage(webapp.RequestHandler):


	def get(self, section):
	
		template_values = {
			'title': 'Welcome', 
			'path': '/idea/%s/' % section,
			'iconf': iconf
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/idea.%s.html' % section)
		self.response.out.write(template.render(path, template_values))
		
