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
import app.fetch

class DDOnline:
	def ssget_feed(self, client='--none--'):
		url = "http://mpmap02.flightgear.org/fg_server_xml.cgi?mpserver02.flightgear.org:5001"
		result = urlfetch.fetch(url)
		if result.status_code == 200:
			
			try:
				doc = xml.dom.minidom.parseString(result.content)
			except :
				print "ERRORsome parse error"
				return None
			
			pilots = {}
			#for node in doc.getElementsByTagName("fg_server"):
				#if node.getAttribute("pilot_cnt"):
					#pilot_cnt = node.getAttribute("pilot_cnt")
			"""
			<marker callsign="barta" server_ip="LOCAL" model="aerostar" 
			slat="-32.738765" lng="-68.782593" alt="2243.647478" 				
			heading="110.946533203125" pitch="0.928494572639465" roll="0.190453231334686" /> 
			"""
			for node in doc.getElementsByTagName("marker"):
				callsign = node.getAttribute("callsign")
				pilots[callsign] = {
							'aero': node.getAttribute("model"), 
							'callsign': callsign, 
							'lat': float(node.getAttribute("lat")), 
							'lng': float(node.getAttribute("lng")), 
							'heading': float(node.getAttribute("heading")),
							'alt': float(node.getAttribute("alt")),
							'server': node.getAttribute("server_ip")

				}
			#data = {'pilots': pilots, 'count': pilot_cnt, 'client': client}
			
			pilots_sorted = []
			for ki in sorted(pilots.keys()):
				pilots_sorted.append( pilots[ki] )
			if not memcache.set("pilots_online", pilots_sorted, 5):
				print "error"
			#data['loaded'] = True
			return pilots_sorted


class OnlinePage(webapp.RequestHandler):

	def get(self):

		subtabs = []
		subtabs.append({'label': 'Plain View', 'page': 'html'})
		subtabs.append({'label': 'Widget View', 'page': 'ajax'})

		page = self.request.get("page")
		if not page:
			page = subtabs[0]['page']

		pilots_online = app.fetch.pilots_online()
		template_values = {
			'conf': conf, 'path': self.request.path, 
			'title': 'Pilots Online', 'subtabs': subtabs, 'page': page,
			'pilots_online': pilots_online
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/online.html')
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
