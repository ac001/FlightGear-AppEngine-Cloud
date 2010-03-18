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

		return

		if section == 'aircraft': # and subpage == "aircraft":
			
			## 
			aero_request = self.request.get("aero")
			if aero_request:
				query = db.GqlQuery("SELECT * FROM  Aero where aero = :1", aero_request) 
				aero = query.get()
				#print "aero=", aero_request, aero.description
				if aero:
					##airdb = Aircraft()
					template_vars['title'] = aero.description
					template_vars['aero'] = aero
					##template_vars['content_template'] = 'aero_include.html'
					##template_vars['path'] =  '/aircraft/'
					##client = app.Issues.GoogleIssuesClient()
					##issues = client.aero(aero.aero)
					#print issues
					##template_vars['issues']  = issues
					##q#uery = db.GqlQuery("SELECT * FROM  AeroFile where directory = :1", aero.directory) 
					##aero_files = query.fetch(20)
					##template_vars['aero_files'] = aero_files

					##template_vars['videos'] = get_videos(selected_aircraft)
					#print template_vars
				else:
					self.redirect("/aircraft/?search=%s" % aero_request)

			else:
				search_text = ""
				airdb = Aircraft()
				if self.request.get("search"):
					search_text = self.request.get("search").lower()
					aircraft = []
					if search_text:
						query = Aero.all()
						dbair = query.fetch(1000)
				
						for aero in dbair:
							#print aero.aero, search_text,  aero.aero.find(search_text)
							if aero.description.lower().find(search_text)  > -1:
								#print "match", search_str
								aircraft.append(aero)
				else:
					aircraft = airdb.get_all()
				
				
				template_vars['title'] = 'Aircraft'
				template_vars['aircraft'] = aircraft 
				template_vars['search_text'] = search_text
