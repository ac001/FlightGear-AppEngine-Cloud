# -*- coding: utf-8 -*-
import os
import cgi
import json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


import conf
from google.appengine.ext import db

from models.models import MPServer

##################################
## Import
class ImportHandler(webapp.RequestHandler):

	def get(self):
		reply = {"no:": self.request.get("no") }
		query = db.GqlQuery("SELECT * FROM  MPServer where no = :1", self.request.get("no")) 
		server = query.get()
	
		x =  "edit"
		if not server:
			x =  "create"
			server = MPServer()
			server.server = self.request.get("server")
		
		server.no = self.request.get("no")
		server.description = self.request.get("description")
		server.host = self.request.get("host")
		server.port = self.request.get("port")
		server.ip = self.request.get("ip")
		server.dev = self.request.get("dev") == "1"
		server.location = self.request.get("location")
		server.put()
		#if not memcache.set("server/%s" % server.server, server):
		#	print "error"
		#data['loaded'] = True
		#return data

		## todo render proper response
		

		
		self.response.out.write(json.dumps(reply))

