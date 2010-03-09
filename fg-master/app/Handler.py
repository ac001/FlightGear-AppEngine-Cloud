# -*- coding: utf-8 -*-
import os
import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


import conf


class HandlerPage(webapp.RequestHandler):


	def get(self, section=None, subpage=None):
	
		template_vars = {}

		## Thconfiguration
		template_vars['conf'] = conf


		## Application Calls Object
		#fgApp = app.FG_App.FG_App()
		#template_vars['app'] = fgApp

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
		#template_vars['title'] = fgApp.title(path)

		
		#######################################
		## Section and subpage handlers
		#######################################

		## Index
		"""if section == 'index':
			if subpage == "announce":
				template_vars['title'] = 'News and Announcements'
			elif subpage == "calendar":
				template_vars['title'] = 'Calendar'
			else:
				pass
		## About
		if section == 'about':
			template_vars['title'] = 'About FlightGear'

		
		## Download 
		if section == 'download':
			if subpage == "versions":
				template_vars['versions'] = app.fetch.versions()
				template_vars['title'] = 'Versions'
			
			elif subpage == "requirements":
				template_vars['title'] = 'Hardware Requirements'
		
			else:
				template_vars['title'] = 'Download Central'
					#sql = "SELECT * FROM DownloadServer ORDER BY location"
					#query = db.GqlQuery(sql)
					#template_vars['download_servers'] = query.fetch(100)
		"""
		## Media#
		"""
		if section == 'media':
			if subpage == "gallery":
				template_vars['title'] = 'Image Gallery'
				template_vars['gallery'] = app.fetch.gallery_thumbs()
			elif subpage == 'videos':
				template_vars['videos_tutorial'] = app.fetch.videos('+FlightGear +tutorial')
				template_vars['videos_howto'] = app.fetch.videos('+flightgear +howto')
			else:
				template_vars['title'] = 'Media'
		"""
		## MultiPlayerr
		"""
		if section == "multiplayer": 
			if subpage == 'pilots':
				template_vars['pilots_online'] = app.fetch.pilots_online()
				template_vars['title'] = 'Pilots Online'

			elif subpage == "servers":
				#servers = app.fetch.mpservers()
				#for srv in servers:
				#	v = memcache.get("server_count_%s" % srv.server)
				#	srv.pilots_count = "-" if v == None else v
				#template_vars['servers'] = servers
				template_vars['title'] = 'Multi Player Servers'
			else:
				template_vars['title'] = 'Multi Player Servers'
		"""

			
		## Download Section
		"""if section == 'download':
			if subpage == "versions":
				template_vars['versions'] = app.fetch.versions()
				template_vars['title'] = 'Versions'
			
			elif subpage == "requirements":
				template_vars['title'] = 'Hardware Requirements'
		"""

		## Media
		"""if section == 'media':
			if subpage == "gallery":
				template_vars['title'] = 'Image Gallery'
				template_vars['gallery'] = app.fetch.gallery_thumbs()
			if subpage == 'videos':
				template_vars['videos_tutorial'] = app.fetch.videos('+FlightGear +tutorial')
				template_vars['videos_howto'] = app.fetch.videos('+flightgear +howto')
			
		if section == "multiplayer": 
			if subpage == 'pilots':
				template_vars['pilots_online'] = app.fetch.pilots_online()
				template_vars['title'] = 'Pilots Online'

			if subpage == "servers":
				servers = app.fetch.mpservers()
				for srv in servers:
					v = memcache.get("server_count_%s" % srv.server)
					srv.pilots_count = "-" if v == None else v
				template_vars['servers'] = servers
				template_vars['title'] = 'Multi Player Servers'

		"""
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
				#template_vars['liveries'] = app.fetch.liveries()




		path = os.path.join(os.path.dirname(__file__), 'templates/%s.html' % section)
		self.response.out.write(template.render(path, template_vars))

######################################################
## Second Generation Down
######################################################
class LashUpSubPage(webapp.RequestHandler):


	def get(self, section, subpage):
		
		fgApp = app.fetch.FGApp()

		template_vars = {}
		if section and subpage:
			path = '/%s/%s/' % (section, subpage)
			main_template = '%s.%s.html' % (section, subpage)
		
		"""
			'path': '/idea/%s/%s/' % (section, subpage),
			'conf': conf,
			'aero': None,
			'app': fgApp
		}"""


		## Media
		if section == 'media':
			if subpage == "gallery":
				template_vars['title'] = 'Image Gallery'
				template_vars['gallery'] = app.fetch.gallery_thumbs()
			if subpage == 'videos':
				template_vars['videos_tutorial'] = app.fetch.videos('+FlightGear +tutorial')
				template_vars['videos_howto'] = app.fetch.videos('+flightgear +howto')
			
		if section == "multiplayer": 
			if subpage == 'pilots':
				template_vars['pilots_online'] = app.fetch.pilots_online()
				template_vars['title'] = 'Pilots Online'

			if subpage == "servers":
				servers = app.fetch.mpservers()
				for srv in servers:
					v = memcache.get("server_count_%s" % srv.server)
					srv.pilots_count = "-" if v == None else v
				template_vars['servers'] = servers
				template_vars['title'] = 'Multi Player Servers'

		

		path = os.path.join(os.path.dirname(__file__), '../templates/MAIN.html')
		self.response.out.write(template.render(path, template_vars))
		


################################################################################
## First Level
################################################################################
class LashUpPage(webapp.RequestHandler):


	def get(self, section):
		fgApp = app.fetch.FGApp()
		template_vars = {
			'path': '/idea/%s/' % section,
			'conf': conf,
			'app': fgApp
		}

		#if section == 'gallery':
		#	template_vars['gallery'] = app.fetch.gallery_thumbs()

		#if section == "multiplayer":
		#		template_vars['servers'] = app.fetch.mpservers()

		if section == "download":
				sql = "SELECT * FROM DownloadServer ORDER BY location"
				query = db.GqlQuery(sql)
				template_vars['download_servers'] = query.fetch(100)
				template_vars['title'] = 'Download Central'

		if section == 'about':
			template_vars['title'] = 'About FlightGear'

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
				#template_vars['liveries'] = app.fetch.liveries()




		path = os.path.join(os.path.dirname(__file__), 'templates/%s.html' % section)
		self.response.out.write(template.render(path, template_vars))

######################################################
## Second Generation Down
######################################################
class LashUpSubPage(webapp.RequestHandler):


	def get(self, section, subpage):
		##print "sec/sub", section, subpage

		fgApp = app.fetch.FGApp()
		template_vars = {
			'title': '####', 
			'path': '/idea/%s/%s/' % (section, subpage),
			'conf': conf,
			'aero': None,
			'app': fgApp
		}

		if section == 'home':
			if subpage == "announce":
				template_vars['title'] = 'News and Announcements'
			
			if subpage == "calendar":
				template_vars['title'] = 'Calendar'
			
		## Download Section
		if section == 'download':
			if subpage == "versions":
				template_vars['versions'] = app.fetch.versions()
				template_vars['title'] = 'Versions'
			
			if subpage == "requirements":
				template_vars['title'] = 'Hardware Requirements'


		## Media
		if section == 'media':
			if subpage == "gallery":
				template_vars['title'] = 'Image Gallery'
				template_vars['gallery'] = app.fetch.gallery_thumbs()
			if subpage == 'videos':
				template_vars['videos_tutorial'] = app.fetch.videos('+FlightGear +tutorial')
				template_vars['videos_howto'] = app.fetch.videos('+flightgear +howto')
			
		if section == "multiplayer": 
			if subpage == 'pilots':
				template_vars['pilots_online'] = app.fetch.pilots_online()
				template_vars['title'] = 'Pilots Online'

			if subpage == "servers":
				servers = app.fetch.mpservers()
				for srv in servers:
					v = memcache.get("server_count_%s" % srv.server)
					srv.pilots_count = "-" if v == None else v
				template_vars['servers'] = servers
				template_vars['title'] = 'Multi Player Servers'

		

		path = os.path.join(os.path.dirname(__file__), 'templates/%s.%s.html' % (section, subpage))
		self.response.out.write(template.render(path, template_vars))
		