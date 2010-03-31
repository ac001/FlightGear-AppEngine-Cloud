# -*- coding: utf-8 -*-
import os
import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.utils import simplejson as json

import conf
import app.FG_Online

## Pulls and updates Pilots and Servers
class UpdateStatus(webapp.RequestHandler):

	def get(self, action=None):
		
		reply = {}
		reply['action'] = action

		if action == 'servers':
			reply['mp_servers_info'] = app.fetch.mpservers_status_update()
			if self.request.get("return"):
				self.redirect("/servers/")

		elif action == 'pilots':
			reply['pilots_info'] = app.fetch.get_pilots_feed()


		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write(json.dumps(reply))

		
					



class FeedHandler(webapp.RequestHandler):

	def get(self, page=None, fetch=None):

		fgOnline = app.FG_Online.FG_Online()
		#print fgOnline.mp_servers_info()
		reply = {'success': True} # this is always true for ext js
		#reply['fetch'] =  page + '_' + fetch

		##############################
		## Servers
		if page == 'servers':
			if fetch == 'info':
				reply['servers_info'] = fgOnline.mp_servers_info()
			elif fetch == 'list':
				reply['servers'] = fgOnline.mp_servers()

		##############################
		## Pilots
		if page == 'pilots':
			if fetch == 'info':
				reply['pilots_info'] = fgOnline.pilots_info()

			elif fetch == 'list':
				reply['pilots'] = fgOnline.pilots_online()

		#reply['section'] =  section

		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write( json.dumps(reply) )

	

class HandlerPage(webapp.RequestHandler):

	def get(self, section=None, subpage=None):
	
		template_vars = {}

		## Thconfiguration
		template_vars['conf'] = conf


		## Application Calls Object
		fgOnline = app.FG_Online.FG_Online()
		template_vars['app'] = fgOnline

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
		template_vars['title'] = fgOnline.title(path)

		

		template_path = os.path.join(os.path.dirname(__file__), '../templates/%s' % main_template)
		self.response.out.write(template.render(template_path, template_vars))
