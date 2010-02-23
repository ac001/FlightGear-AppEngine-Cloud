# -*- coding: utf-8 -*-
import os
import sys
import datetime

from django.utils import simplejson as json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import memcache
from google.appengine.ext import db

from google.appengine.api import urlfetch
import xml.dom.minidom

import gdata.youtube.service
#import gdata.projecthosting.data
#import gdata.gauth
#import gdata.client
#import gdata.data
import atom.http_core
import atom.core


from models.models import Aero
from models.models import AeroFile
from models.models import Developer

import app.Issues

import conf

class Aircraft:

	def get_all(self):

		data = memcache.get("aircraft_all")
		if data is not None:
			return data

		query = Aero.all()
		aircraft = query.fetch(10000)

		aircraft_list = {}
		for aero in aircraft:
			aircraft_list[aero.aero] = aero.description
		if not memcache.set("aircraft_list", data, 5):
			print "error=aircraft_list"
		
		if not memcache.set("aircraft_all", data, 5):
			print "error=aircraft_all"

		return aircraft

	def aircraft_list(self):
		data = memcache.get("aircraft_list")
		if data == None:
			self.get_all()
		return memcache.get("aircraft_list")

	def search(self, search_str=None):
		aircraft = self.get_all()
		aircraft_list = []
		for aero in aircraft:
			#print aero.aero, search_str,  aero.aero.find(search_str)
			if aero.aero.find(search_str)  > -1:
				#print "match", search_str
				aircraft_list.append(aero)
			#print aero
		return aircraft_list

def get_videos( aero):
	client = gdata.youtube.service.YouTubeService()
	query = gdata.youtube.service.YouTubeVideoQuery()
	query.vq = "flightgear " + aero
	query.max_results = 10
	#query.order_by = "rating"
	feed = client.YouTubeQuery(query)	
	#print feed
	videos = []
	for entry in feed.entry:
		v = process_vid_entry(entry)
		videos.append(v)
	return videos

def process_vid_entry( entry):
	dic = {}
	dic['id'] = entry.id.text.split("/")[-1]
	dic['title'] = entry.title.text
	dic['thumbnail'] = entry.media.thumbnail[0].url
	#print dic
	#dic['stars'] = issue.stars.text
	#dic['state'] = issue.state.text
	#dic['status'] = issue.status.text
	return dic


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
				airdb = Aircraft()
				template_values['title'] = aero.description
				template_values['aero'] = aero
				template_values['content_template'] = 'aero_include.html'
				template_values['path'] =  '/aircraft/'
				client = app.Issues.GoogleIssuesClient()
				issues = client.aero(aero.aero)
				#print issues
				template_values['issues']  = issues
				query = db.GqlQuery("SELECT * FROM  AeroFile where directory = :1", aero.directory) 
				aero_files = query.fetch(1000)
				template_values['aero_files'] = aero_files

				template_values['videos'] = get_videos(selected_aircraft)
				#print template_values
			else:
				self.redirect("/aircraft/?search=%s" % selected_aircraft)

		else:
			""" Show all aircraft or searched"""
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
			template_values['content_template'] = 'aircraft_include.html'
			template_values['path'] =  '/aircraft/'
		
		path = os.path.join(os.path.dirname(__file__), 'templates/aircraft.html')
		self.response.out.write(template.render(path, template_values))



class AircraftImport(webapp.RequestHandler):
	
	def post(self):

		template_values = {
			#'pilots_online': self.get_pilots()
		}
		query = db.GqlQuery("SELECT * FROM  Aero where aero = :1", self.request.get("aero")) 
		aero = query.get()
		if not aero:
			x =  "add"
			aero = Aero()
			aero.aero = self.request.get("aero")
			aero.author = self.request.get("author")
			aero.directory = self.request.get("directory")
			aero.description = self.request.get("description")
			aero.status = self.request.get("status")
			aero.fdm = self.request.get("flight-model")
			aero.splash = self.request.get("splash")
			aero.version = self.request.get("version")
			aero.splash = self.request.get("splash")
			aero.put()
		else:
			x = "edit"
			pass



		reply = {'success': True, 'status': x}
		#print 'Content-Type: text/plain'
		#print ''
		#print json.dumps(self.get_pilots())
		#path = os.path.join(os.path.dirname(__file__), 'templates/pilots_online.html')
		self.response.out.write(json.dumps(reply))



class AircraftImportRevisions(webapp.RequestHandler):
	
	def post(self):

		revisions =  json.loads(self.request.get("revisions"))
		ret = {}
		c = 0
		for dic in revisions:
			cfile = dic['file']
			rev_dic = dic['revision']

			query = db.GqlQuery("SELECT * FROM  AeroFile where directory = :1 and file_name = :2", cfile['directory'], cfile['file_name'])
			fileOb = query.get()
			if not fileOb:

				dated = datetime.datetime.strptime(rev_dic['date'], "%Y/%m/%d %H:%M:%S") #"date": "2008/09/22 23:08:47"
				fileOb = AeroFile()
				fileOb.file_name = cfile['file_name']
				fileOb.directory = cfile['directory']
				fileOb.revision = rev_dic['revision']
				fileOb.message = rev_dic['message']
				fileOb.updated = dated
				fileOb.put()

			#### revision
			

			## check author
			query = db.GqlQuery("SELECT * FROM  Developer where cvs = :1", rev_dic['author'])
			devOb = query.get()
			if not devOb:
				devOb = Developer()	
				devOb.cvs = rev_dic['author']
				devOb.put()

			
			#query = db.GqlQuery("SELECT * FROM  Revision where aero_file = :parent", parent=fileOb.key())
			#revOb = query.get()
			#create_rev = False
			#if revOb:
				#if revOb.revision == rev_dic['revision']:
					#print "skip"
					#create_rev = False
				#else:
					#create_rev = True
					#revOb.revision == rev_dic['revision']
			#else:
				#create_rev = True

			#if create_rev:
				#revOb = Revision(parent=fileOb)	
				#revOb.aero_file = fileOb
				#revOb.dev = devOb

				#revOb.put()		



class AircraftRpc(webapp.RequestHandler):

	def post(self):
		self.get()

	def get(self, selected_aircraft=None):
		
		template_values = {
			'conf': conf
		}
		search_text = self.request.get("query")
		aircraft_list = []
		if search_text:
			query = Aero.all()
			aircraft = query.fetch(1000)
			
			for aero in aircraft:
				#print aero.aero, search_text,  aero.aero.find(search_text)
				if aero.aero.find(search_text)  > -1:
					#print "match", search_str
					aircraft_list.append({'aero': aero.aero, 'description': aero.description})

		payload = {'success': True, 'aircraft': aircraft_list, 'count': len(aircraft_list)}
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write(json.dumps(payload))