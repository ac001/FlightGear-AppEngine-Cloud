# -*- coding: utf-8 -*-
import os
import sys
from django.utils import simplejson as json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import memcache
from google.appengine.ext import db

from google.appengine.api import urlfetch
import xml.dom.minidom


from models.models import Aero
from models.models import AeroFile
from models.models import Developer
from models.models import Revision

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
				query = db.GqlQuery("SELECT * FROM  AeroFile where directory = :1", aero.directory) 
				aero_files = query.fetch(1000)
				template_values['aero_files'] = aero_files
				

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



class AircraftImport(webapp.RequestHandler):
	
	def post(self):

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
			x = "edit"
			pass

		aero.author = self.request.get("author")
		aero.directory = self.request.get("directory")
		aero.description = self.request.get("description")
		aero.status = self.request.get("status")
		aero.fdm = self.request.get("flight-model")
		aero.splash = self.request.get("splash")
		aero.version = self.request.get("version")
		aero.splash = self.request.get("splash")
		aero.put()

		reply = {'success': True, 'status': x}
		#print 'Content-Type: text/plain'
		#print ''
		#print json.dumps(self.get_pilots())
		#path = os.path.join(os.path.dirname(__file__), 'templates/pilots_online.html')
		self.response.out.write(json.dumps("ok"))



class AircraftImportRevisions(webapp.RequestHandler):
	
	def post(self):

		revisions =  json.loads(self.request.get("revisions"))
		ret = {}
		c = 0
		for dic in revisions:
			cfile = dic['file']
			query = db.GqlQuery("SELECT * FROM  AeroFile where directory = :1 and file_name = :2", cfile['directory'], cfile['file_name'])
			fileOb = query.get()
			if not fileOb:
				fileOb = AeroFile()
				fileOb.file_name = cfile['file_name']
				fileOb.directory = cfile['directory']
				fileOb.rcs = cfile['rcs']
				fileOb.head = cfile['head']
				fileOb.put()

			#### revision
			rev_dic = dic['revision']

			## check author
			query = db.GqlQuery("SELECT * FROM  Developer where cvs = :1", rev_dic['author'])
			devOb = query.get()
			if not devOb:
				devOb = Developer()	
				devOb.cvs = rev_dic['author']
				devOb.put()

			
			query = db.GqlQuery("SELECT * FROM  Revision where aero_file = :parent", parent=fileOb.key())
			revOb = query.get()
			create_rev = False
			if revOb:
				if revOb.revision == rev_dic['revision']:
					print "skip"
					create_rev = False
				else:
					create_rev = True
					#revOb.revision == rev_dic['revision']
			else:
				create_rev = True

			if create_rev:
				revOb = Revision(parent=fileOb)	
				#revOb.aero_file = fileOb
				revOb.dev = devOb
				revOb.revision = rev_dic['revision']
				revOb.message = rev_dic['message']
				revOb.put()		
			c += 1
			#if c == 8:
				#sys.exit(0)
		"""
{"file": {"directory": "707", "file_name": " 707-338.txt", "head": " 1.1", "rcs": " /var/cvs/FlightGear-0.9/data/Aircraft/707/707-338.txt,v"}, "revision": {"date": "2006/01/04 12:41:45", "state": "Exp", "revision": "1.1", "message": "Add Innis' Boeing 707 model.", "author": "ehofman"}},

		lambda x: datetime.datetime.strptime(x, '%m/%d/%Y').date()),

		class AeroFile(db.Model):
			file_name = db.StringProperty()
			head = db.StringProperty()
			rcs = db.StringProperty()
			revision = db.StringProperty()
			last_update = db.DateTimeProperty()
		"""
		#results = query.fetch(10)
		#c =  query.count()
		foo  ={}
		#print results
		#aero = query.get()
		#for res in results:
		#	foo[res.aero] = "foo"
		#if not aero:
			#x =  "create"
			#aero = Aero()
			#aero.aero = self.request.get("aero")
		#else:
			#x = "edit"
			#pass


		#aero.put()

		#reply = {'success': True, 'status': x}

		self.response.out.write(ret)


