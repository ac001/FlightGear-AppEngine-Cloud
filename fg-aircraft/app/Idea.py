# -*- coding: utf-8 -*-
import os
import cgi

#from google.appengine.api import users

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
#from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import memcache
from google.appengine.ext import db

import conf
import app.fetch
from app.Aircraft import Aircraft
from models.models import Aero

from models.models import DownloadServer


class IdeaPage(webapp.RequestHandler):


	def get(self):
	
		template_values = {
			'title': 'Welcome', 
			'path': '/idea/',
			'conf': conf,
			'random_image': app.fetch.gallery_random(),
			'servers': app.fetch.mpservers()
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/MAIN.html')
		self.response.out.write(template.render(path, template_values))
		


################################################################################
## First Level
################################################################################
class LashUpPage(webapp.RequestHandler):


	def get(self, section):
		fgApp = app.fetch.FGApp()
		template_values = {
			'path': '/idea/%s/' % section,
			'conf': conf,
			'app': fgApp
		}

		#if section == 'gallery':
		#	template_values['gallery'] = app.fetch.gallery_thumbs()

		#if section == "multiplayer":
		#		template_values['servers'] = app.fetch.mpservers()

		if section == "download":
				sql = "SELECT * FROM DownloadServer ORDER BY location"
				query = db.GqlQuery(sql)
				template_values['download_servers'] = query.fetch(100)
				template_values['title'] = 'Download Central'

		if section == 'about':
			template_values['title'] = 'About FlightGear'

		if section == 'aircraft': # and subpage == "aircraft":
			
			## 
			aero_request = self.request.get("aero")
			if aero_request:
				query = db.GqlQuery("SELECT * FROM  Aero where aero = :1", aero_request) 
				aero = query.get()
				#print "aero=", aero_request, aero.description
				if aero:
					##airdb = Aircraft()
					template_values['title'] = aero.description
					template_values['aero'] = aero
					##template_values['content_template'] = 'aero_include.html'
					##template_values['path'] =  '/aircraft/'
					##client = app.Issues.GoogleIssuesClient()
					##issues = client.aero(aero.aero)
					#print issues
					##template_values['issues']  = issues
					##q#uery = db.GqlQuery("SELECT * FROM  AeroFile where directory = :1", aero.directory) 
					##aero_files = query.fetch(20)
					##template_values['aero_files'] = aero_files

					##template_values['videos'] = get_videos(selected_aircraft)
					#print template_values
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
				
				
				template_values['title'] = 'Aircraft'
				template_values['aircraft'] = aircraft 
				template_values['search_text'] = search_text
				#template_values['liveries'] = app.fetch.liveries()




		path = os.path.join(os.path.dirname(__file__), 'templates/%s.html' % section)
		self.response.out.write(template.render(path, template_values))

######################################################
## Second Generation Down
######################################################
class LashUpSubPage(webapp.RequestHandler):


	def get(self, section, subpage):
		##print "sec/sub", section, subpage

		fgApp = app.fetch.FGApp()
		template_values = {
			'title': '####', 
			'path': '/idea/%s/%s/' % (section, subpage),
			'conf': conf,
			'aero': None,
			'app': fgApp
		}

		if section == 'home':
			if subpage == "announce":
				template_values['title'] = 'News and Announcements'
			
			if subpage == "calendar":
				template_values['title'] = 'Calendar'
			
		## Download Section
		if section == 'download':
			if subpage == "versions":
				template_values['versions'] = app.fetch.versions()
				template_values['title'] = 'Versions'
			
			if subpage == "requirements":
				template_values['title'] = 'Hardware Requirements'


		## Media
		if section == 'media':
			if subpage == "gallery":
				template_values['title'] = 'Image Gallery'
				template_values['gallery'] = app.fetch.gallery_thumbs()
			if subpage == 'videos':
				template_values['videos_tutorial'] = app.fetch.videos('+FlightGear +tutorial')
				template_values['videos_howto'] = app.fetch.videos('+flightgear +howto')
			
		if section == "multiplayer": 
			if subpage == 'pilots':
				template_values['pilots_online'] = app.fetch.pilots_online()
				template_values['title'] = 'Pilots Online'

			if subpage == "servers":
				servers = app.fetch.mpservers()
				for srv in servers:
					v = memcache.get("server_count_%s" % srv.server)
					srv.pilots_count = "-" if v == None else v
				template_values['servers'] = servers
				template_values['title'] = 'Multi Player Servers'

		

		path = os.path.join(os.path.dirname(__file__), 'templates/%s.%s.html' % (section, subpage))
		self.response.out.write(template.render(path, template_values))
		