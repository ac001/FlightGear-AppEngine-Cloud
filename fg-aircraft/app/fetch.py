# -*- coding: utf-8 -*-

import datetime

from google.appengine.ext import db
from google.appengine.api import memcache

from google.appengine.api import urlfetch
import xml.dom.minidom

from BeautifulSoup import BeautifulSoup 

import conf
from models.models import MPServer

####################################################
## Pilots Online
####################################################
def pilots_online():
	data = memcache.get("pilots_online")
	if data is not None:
		return data
	return update_pilots_feed()

def pilots_info():
	data = memcache.get("pilots_info")
	if data is not None:
		return data
	update_pilots_feed()
	return memcache.get("pilots_info")

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
			player_ips = {}
			servers_lookup = server_ip_lookup()

			for node in doc.getElementsByTagName("marker"):
				callsign = node.getAttribute("callsign")
				ip = node.getAttribute("server_ip")
				if servers_lookup.has_key(ip):
					server = servers_lookup[ip]
				else:
					server = ip
				pilots[callsign] = {
							'aero': node.getAttribute("model"), 
							'callsign': callsign, 
							'lat': float(node.getAttribute("lat")), 
							'lng': float(node.getAttribute("lng")), 
							'heading': float(node.getAttribute("heading")),
							'alt': float(node.getAttribute("alt")),
							'server': server
				}
				if player_ips.has_key(server):
					player_ips[server] += 1
				else:
					player_ips[server] = 1
			#print player_ips
			#servers = server_ips()
			for server in player_ips:
				if not memcache.set("server_count_%s" % server, player_ips[server]):
					print "fail"
			


			callsigns =  sorted(pilots.keys())
			if not memcache.set("callsigns", callsigns, 10):
				print "error"
			info = {'count': len(callsigns), 'updated': datetime.datetime.now()}
			if not memcache.set("pilots_info", info, 10):
				print "error"

			pilots_sorted = []
			for ki in callsigns:
				pilots_sorted.append( pilots[ki] )
			if not memcache.set("pilots_online", pilots_sorted, 20):
				print "error"

			return pilots_sorted


####################################################
## MP Server
####################################################
def mpservers():
	data = memcache.get("mp_servers")
	if data is not None:
		return data
	query = db.GqlQuery("SELECT * FROM MPServer order by no asc")
	data = query.fetch(100)
	if not memcache.set("mp_servers", data, 120):
		print "error"
	return data

def mpservers_info():
	info =	memcache.get("mpservers_info")
	last = info['updated']	
	current = datetime.datetime.now()
	info['ago'] =  last - current
	return info

def server_ip_lookup():
	servers = mpservers()
	ret = {}
	local = ''
	for server in servers:
		ret[server.ip] = server.server
		if server.server == "mpserver02":
			ret['LOCAL'] = server.server
		else:
			ret[server.ip] = server.server
	return ret

def mpservers_status_update():
	""" Parses out the http://mpmap01.flightgear.org/mpstatus/ page """

	## fetch content 
	result = urlfetch.fetch(conf.MP_STATUS_URL)
	if result.status_code == 200:
			
		soup = BeautifulSoup.BeautifulSoup(result.content)
		
		## find all tables
		tables = soup.findAll('table')

		## Parse the MP status ie first table.. 3 cols = descripioon, "-" and OK or Down
		rows =  tables[0].findAll(['tr'])

		## Loop rows and update local store
		up = 0
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
					up += 1
					server.status_updated = datetime.datetime.now()
					server.put()
				else:
					down += 1
				
		info = {'updated': datetime.datetime.now(), 'up': up, 'down': down, 'total': up + down}
		memcache.set("mpservers_info", info)
		return True


