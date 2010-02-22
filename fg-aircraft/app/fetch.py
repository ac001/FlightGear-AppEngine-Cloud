# -*- coding: utf-8 -*-

from google.appengine.api import memcache
from google.appengine.api import urlfetch
import xml.dom.minidom

import conf

def pilots_online():
	data = memcache.get("pilots_online")
	if data is not None:
		return data
	return update_pilots_feed()

def pilots_count():
	data = memcache.get("pilots_count")
	if data is not None:
		return data
	update_pilots_feed()
	return memcache.get("pilots_count")

def update_pilots_feed():
		url = conf.MP_PILOTS_URL
		result = urlfetch.fetch(url)
		if result.status_code == 200:
			
			try:
				doc = xml.dom.minidom.parseString(result.content)
			except :
				print "ERRORsome parse error"
				return None
			
			pilots = {}		
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
			
			pilots_sorted = []
			callsigns =  sorted(pilots.keys())

			if not memcache.set("callsigns", callsigns, 10):
				print "error"
			if not memcache.set("pilots_count", len(callsigns), 10):
				print "error"

			for ki in callsigns:
				pilots_sorted.append( pilots[ki] )
			if not memcache.set("pilots_online", pilots_sorted, 5):
				print "error"

			return pilots_sorted

