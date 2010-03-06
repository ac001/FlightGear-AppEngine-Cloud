# -*- coding: utf-8 -*-
import os
import cgi

#from google.appengine.api import users

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
#from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import memcache

import conf
import app.fetch

class IdeaPage(webapp.RequestHandler):


	def get(self):
	
		template_values = {
			'title': 'Welcome', 
			'path': '/idea/',
			'conf': conf,
			'random_image': app.fetch.gallery_random(),
			'servers': app.fetch.mpservers()
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/idea.html')
		self.response.out.write(template.render(path, template_values))
		



class LashUpPage(webapp.RequestHandler):


	def get(self, section):
	
		template_values = {
			'title': 'Welcome', 
			'path': '/idea/%s/' % section,
			'conf': conf
		}

		if section == 'gallery':
			template_values['gallery'] = app.fetch.gallery_thumbs()

		if section == "multiplayer":
				template_values['servers'] = app.fetch.mpservers()


		path = os.path.join(os.path.dirname(__file__), 'templates/idea.%s.html' % section)
		self.response.out.write(template.render(path, template_values))
		
class LashUpSubPage(webapp.RequestHandler):


	def get(self, section, subpage):
		##print "sec/sub", section, subpage
		template_values = {
			'title': 'Welcome', 
			'path': '/idea/%s/%s/' % (section, subpage),
			'conf': conf
		}



		if section == 'download' and subpage == "versions":
			template_values['versions'] = app.fetch.versions()

		if section == "multiplayer": 
			if subpage == 'pilots':
				template_values['pilots_online'] = app.fetch.pilots_online()

			if subpage == "servers":
				servers = app.fetch.mpservers()
				for srv in servers:
					v = memcache.get("server_count_%s" % srv.server)
					srv.pilots_count = "-" if v == None else v
				template_values['servers'] = servers



		path = os.path.join(os.path.dirname(__file__), 'templates/idea.%s.%s.html' % (section, subpage))
		self.response.out.write(template.render(path, template_values))
		