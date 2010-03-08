# -*- coding: utf-8 -*-
import os
import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.utils import simplejson as json

import conf
import app.FG_Online

class UpdateStatus(webapp.RequestHandler):

	def get(self, action=None):

		app.fetch.mpservers_status_update()
		if self.request.get("return"):
			self.redirect("/servers/")
		else:
			self.response.out.write(json.dumps({'update': 'ok'}))

		

class RPCHandler(webapp.RequestHandler):

	def get(self, action=None):

		fgOnline = app.FG_Online.FG_Online()

		reply = {'success': True} # this is always true for ext js
		reply['data'] = fgOnline.mp_servers_json_feed()

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
