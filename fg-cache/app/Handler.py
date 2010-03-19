# -*- coding: utf-8 -*-

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class HandlerPage(webapp.RequestHandler):


	def get(self):
	
		template_vars = {}
	

		template_path = os.path.join(os.path.dirname(__file__), '../templates/%s' % "MAIN.html")
		self.response.out.write(template.render(template_path, template_vars))

