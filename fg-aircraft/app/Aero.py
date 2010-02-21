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

class AeroPage(webapp.RequestHandler):

	def get(self, aero):
		
		query = db.GqlQuery("SELECT * FROM  Aero where aero = :1", aero) 
		aeroObj = query.get()

		template_values = {
			'title': 'Aircraft', 'aero': aeroObj
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/aero.html')
		self.response.out.write(template.render(path, template_values))



class AeroRpc(webapp.RequestHandler):
	

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
		aero.put()

		#print 'Content-Type: text/plain'
		#print ''
		#print json.dumps(self.get_pilots())
		#path = os.path.join(os.path.dirname(__file__), 'templates/pilots_online.html')
		self.response.out.write(json.dumps(foo))


