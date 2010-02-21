# -*- coding: utf-8 -*-
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import memcache

from google.appengine.api import urlfetch
import xml.dom.minidom

class PilotsOnline(webapp.RequestHandler):

	def get_pilots(self):
		data = memcache.get("pilots_online")
		if data is not None:
			return data

		url = "http://mpmap02.flightgear.org/fg_server_xml.cgi?mpserver02.flightgear.org:5001"
		result = urlfetch.fetch(url)
		if result.status_code == 200:
			
			try:
				doc = xml.dom.minidom.parseString(result.content)
			except :
				print "ERRORsome parse error"
				return
			
			#print "LOAAD", doc
			pilots = {}
			for node in doc.getElementsByTagName("fg_server"):
				#if node.getAttribute("pilot_cnt"):
					pilot_cnt = node.getAttribute("pilot_cnt")
			for node in doc.getElementsByTagName("marker"):
				#if node.getAttribute("pilot_cnt"):
				pilots[node.getAttribute("callsign")] = {'model': node.getAttribute("model") }
			data = {'pilots': pilots, 'count': pilot_cnt}
			
			if not memcache.set("pilots_online", data, 10):
				print "error"
			data['loaded'] = True
			return data


	def get(self):

		template_values = {
			'pilots_online': self.get_pilots()
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/pilots_online.html')
		self.response.out.write(template.render(path, template_values))
		
