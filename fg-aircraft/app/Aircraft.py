# -*- coding: utf-8 -*-
import os
from django.utils import simplejson as json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import memcache
from google.appengine.ext import db

from google.appengine.api import urlfetch
import xml.dom.minidom

from models.models import Aero
import app.Issues

import conf

class Aircraft:

	def get_all(self):

		data = memcache.get("aircraft_all")
		if data is not None:
			return data, True

		query = Aero.all()
		aircraft = query.fetch(10000)

		aircraft_list = {}
		for aero in aircraft:
			aircraft_list[aero.aero] = aero.description
		if not memcache.set("aircraft_list", data, 5):
			print "error=aircraft_list"
		
		if not memcache.set("aircraft_all", data, 5):
			print "error=aircraft_all"

		return aircraft, False

	def list_aircraft(self):
		data = memcache.get("aircraft_list")
		self.get_all()
		return memcache.get("aircraft_list")

	def search(self, search_str=None):
		aircraft, cached = self.get_all()
		aircraft_list = []
		for aero in aircraft:
			#print aero.aero, search_str,  aero.aero.find(search_str)
			if aero.aero.find(search_str)  > -1:
				#print "match", search_str
				aircraft_list.append(aero)
			#print aero
		return aircraft_list, False
	

class AircraftPage(webapp.RequestHandler):

	def get(self, selected_aircraft=None):
		
		template_values = {
			'conf': conf
		}

		if selected_aircraft:
			query = db.GqlQuery("SELECT * FROM  Aero where aero = :1", selected_aircraft) 
			aero = query.get()
			#print "aero=", aero
			if aero:
				template_values['title'] = aero.aero
				template_values['aero'] = aero
				template_values['content_template'] = 'aero_include.html'
				template_values['path'] =  '/aircraft/'
				client = app.Issues.GoogleIssuesClient()
				issues = client.aero(aero.aero)
				#print issues
				template_values['issues']  = issues
			

		else:
			""" Show all aircraft or searched"""
			airdb = Aircraft()
			if self.request.get("search"):
				aircraft, cached = airdb.search(self.request.get("search"))
			else:
				aircraft, cached = airdb.get_all()
			
			
			template_values['title'] = 'Aircraft##'
			template_values['aircraft'] = aircraft
			template_values['cached'] = cached, 
			template_values['content_template'] = 'aircraft_include.html'
			template_values['path'] =  '/aircraft/'
		
		path = os.path.join(os.path.dirname(__file__), 'templates/aircraft.html')
		self.response.out.write(template.render(path, template_values))



class AircraftRpc(webapp.RequestHandler):
	

	def BBget(self):

		template_values = {
			#'pilots_online': self.get_pilots()
		}
		aircraft = Aero()
		

		#print 'Content-Type: text/plain'
		#print ''
		#print json.dumps(self.get_pilots())
		#path = os.path.join(os.path.dirname(__file__), 'templates/pilots_online.html')
		self.response.out.write(aircraft)

	def get(self):

		template_values = {
			#'pilots_online': self.get_pilots()
		}
		query = db.GqlQuery("SELECT * FROM  Aero where aero = :1", self.request.get("aero")) 
		#results = query.fetch(10)
		#c =  query.count()
		foo  ={}
		#print results
		aero = query.get()
		#for res in results:
		#	foo[res.aero] = "foo"
		if not aero:
			x =  "create"
			aero = Aero()
			aero.aero = self.request.get("aero")
		else:
			#x = "edit"
			pass
		aero.author = self.request.get("author")
		aero.description = self.request.get("description")
		aero.status = self.request.get("status")
		aero.fdm = self.request.get("flight-model")
		aero.splash = self.request.get("splash")
		aero.version = self.request.get("version")
		aero.splash = self.request.get("splash")
		aero.put()

		#print 'Content-Type: text/plain'
		#print ''
		#print json.dumps(self.get_pilots())
		#path = os.path.join(os.path.dirname(__file__), 'templates/pilots_online.html')
		self.response.out.write(json.dumps(foo))


