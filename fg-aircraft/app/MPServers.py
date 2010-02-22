# -*- coding: utf-8 -*-
import os
from django.utils import simplejson as json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import memcache

from google.appengine.api import urlfetch
import xml.dom.minidom

import conf


class MPServers(webapp.RequestHandler):

	def get_pilots(self):
		data = memcache.get("pilots_online")
		if data is not None:
			return data
		return get_pilots_feed('request')
		

	def get(self):
		template_values = {
			'conf': conf, 'path': self.request.path
		}
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
			'pilots_online': self.get_pilots()
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
