# -*- coding: utf-8 -*-

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import conf
import app.FG_App

class HandlerPage(webapp.RequestHandler):


	def get(self, section=None, subpage=None):
	
		template_vars = {}

		## configuration
		template_vars['conf'] = conf


		## Application Calls Object
		fgApp = app.FG_App.FG_App()
		template_vars['app'] = fgApp
		fgApp.gallery()

		## Set up the enviroment based on section/subpage eg /download/scenery/
		if section == None:
			section = "index"
		if section and subpage:
			path = '/%s/%s/' % (section, subpage)
			main_template = '%s.%s.html' % (section, subpage)
		elif section:
			path = '/%s/' % (section)
			main_template = '%s.html' % (section)
			
		template_vars['path'] = path
		template_vars['title'] = fgApp.title(path)

		

		template_path = os.path.join(os.path.dirname(__file__), '../templates/%s' % main_template)
		self.response.out.write(template.render(template_path, template_vars))

