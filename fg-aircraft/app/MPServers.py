# -*- coding: utf-8 -*-
import os
from django.utils import simplejson as json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import memcache
from google.appengine.ext import db

from google.appengine.api import urlfetch
import datetime

import conf
import app.fetch
#from models.models import MPServer


##################################
## MP servers Index
class MPServersPage(webapp.RequestHandler):

	def get(self, action=None):
		servers = app.fetch.mpservers()
		for srv in servers:
			v = memcache.get("server_count_%s" % srv.server)
			srv.pilots_count = "-" if v == None else v
		template_values = {
			'conf': conf, 'path': self.request.path, 'title': 'MP Servers',
			'servers': servers
		}

		path = os.path.join(os.path.dirname(__file__), 'templates/mpservers.html')
		self.response.out.write(template.render(path, template_values))


##################################
## Import
class MPServerImport(webapp.RequestHandler):

	def get(self):

		template_values = {
			'conf': conf, 'path': '/mpservers/', 'title': 'MP Server import #######'
		}

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
		print "id=", self.request.get("id")

		path = os.path.join(os.path.dirname(__file__), 'templates/mpservers.html')
		self.response.out.write("id=" + x )#template.render(path, template_values))


##################################
## MP Update Server Status
class MPServersUpdateStatus(webapp.RequestHandler):

	def get(self, action=None):

		app.fetch.mpservers_status_update()
		if self.request.get("return"):
			self.redirect("/mpservers/")
		return
		""" Paarses out the http://mpmap01.flightgear.org/mpstatus/ page """
		from BeautifulSoup import BeautifulSoup 
		
		## fetch content 
		result = urlfetch.fetch(conf.MP_STATUS_URL)
		if result.status_code == 200:
				
			soup = BeautifulSoup.BeautifulSoup(result.content)
			
			## find all tables
			tables = soup.findAll('table')
			
			## Parse the MP status ie first table.. 3 cols = descripioon, "-" and OK or Down
			rows =  tables[0].findAll(['tr'])

			## Loop rows and update local store
			online = 0
			down = 0
			for row in rows:			
				cells = row.findAll('td')
				server_name = cells[0].text.split(" ", 1)[0] 
				status = cells[2].text  

				query = db.GqlQuery("SELECT * FROM  MPServer where host = :1", server_name) 
				server = query.get()
				if not server:
					print "NOT= server error"
				else:
					server.status = status
					if status == "OK":
						online += 1
						server.status_updated = datetime.datetime.now()
					else:
						down += 1
					server.put()
		status_info = {'updated': datetime.datetime.now(), 'up': online, 'down': down, 'total': online + down}
		if not memcache.set("status_info", status_info):
			print "memcache error"

		print "all done"
		return
		query = MPServer.all()
		servers = query.fetch(10000)
		#print servers
		template_values = {
			'conf': conf, 'path': '/mpservers/', 'title': 'MP Servers Database',
			'servers': servers
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/mpservers.html')
		self.response.out.write(template.render(path, template_values))




##################################
## MP servers Index
class MPServerPage(webapp.RequestHandler):

	def get(self, var):

		template_values = {
			'conf': conf, 'path': '/mpservers/', 'title': 'MP Server'
		}
		#print "action=", action
		path = os.path.join(os.path.dirname(__file__), 'templates/mpservers.html')
		self.response.out.write(template.render(path, template_values))



class MPServersRpc(webapp.RequestHandler):

	def get_pilots(self):
		data = memcache.get("pilots_online")
		if data is not None:
			return data

		return get_pilots_feed('request')
		

	def get(self):

		template_values = {
			#'pilots_online': self.get_pilots()
		}
		#print 'Content-Type: text/plain'
		#print ''
		print json.dumps(self.get_pilots())
		#path = os.path.join(os.path.dirname(__file__), 'templates/pilots_online.html')
		self.response.out.write(json.dumps(self.get_pilots()))
"""	
class PilotsOnlineCron(webapp.RequestHandler):

	def get(self):
		foo = get_pilots_feed('cron')

		print 'Content-Type: text/plain'
		print ''
		print '{success: true}'

		#template_values = {
		#	'pilots_online': self.get_pilots()
		#}
		path = os.path.join(os.path.dirname(__file__), 'templates/pilots_online.html')
		self.response.out.write(template.render(path, template_values))
"""	
