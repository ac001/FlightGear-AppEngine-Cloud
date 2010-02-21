# -*- coding: utf-8 -*-
import os
from django.utils import simplejson as json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import memcache

from google.appengine.api import urlfetch
import xml.dom.minidom

def get_pilots_feed(client='--none--'):
	url = "http://mpmap02.flightgear.org/fg_server_xml.cgi?mpserver02.flightgear.org:5001"
	result = urlfetch.fetch(url)
	if result.status_code == 200:
		
		try:
			doc = xml.dom.minidom.parseString(result.content)
		except :
			print "ERRORsome parse error"
			return None
		
		#print "LOAAD", doc
		pilots = {}
		for node in doc.getElementsByTagName("fg_server"):
			#if node.getAttribute("pilot_cnt"):
				pilot_cnt = node.getAttribute("pilot_cnt")
		for node in doc.getElementsByTagName("marker"):
			#if node.getAttribute("pilot_cnt"):
			pilots[node.getAttribute("callsign")] = {'model': node.getAttribute("model") }
		data = {'pilots': pilots, 'count': pilot_cnt, 'client': client}
		
		if not memcache.set("pilots_online", data, 5):
			print "error"
		data['loaded'] = True
		return data
	return None

class PilotsOnline(webapp.RequestHandler):

	def get_pilots(self):
		data = memcache.get("pilots_online")
		if data is not None:
			return data
		return get_pilots_feed('request')
		

	def get(self):
		template_values = {
			'pilots_online': self.get_pilots()
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/pilots_online.html')
		self.response.out.write(template.render(path, template_values))

class PilotsOnlineRpc(webapp.RequestHandler):

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
