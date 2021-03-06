# -*- coding: utf-8 -*-

import datetime
import random

from google.appengine.ext import db
from google.appengine.api import memcache


from django.utils import simplejson as json
from google.appengine.api import urlfetch
import xml.dom.minidom

from BeautifulSoup import BeautifulSoup 
"""
import gdata.projecthosting.client
import gdata.projecthosting.data
"""
"""
import gdata.youtube.service
import gdata.gauth
import gdata.client
import gdata.data
import atom.http_core
import atom.core
"""

import conf
from models.models import MPServer




####################################################
## Pilots Online
####################################################
def pilots_online():
	if 1 == 0:
		data = memcache.get("pilots_online")
		if data is not None:
			return data
	return get_pilots_feed()

def atc_online():
	if 1 == 0:
		data = memcache.get("atc_online")
		if data is not None:
			return data
	return memcache.get("atc_online")

def pilots_info():
	data = memcache.get("pilots_info")
	if data is not None:
		return data
	get_pilots_feed()
	return memcache.get("pilots_info")

def get_pilots_feed():
		url = conf.MP_PILOTS_URL
		result = urlfetch.fetch(url)
		if result.status_code == 200:
			
			try:
				doc = xml.dom.minidom.parseString(result.content)
			except :
				print "ERRORsome parse error"
				return None

			
			pilots = {}		
			atc = {}
			player_ips = {}
			servers_lookup = server_ip_lookup()

			for node in doc.getElementsByTagName("marker"):
				callsign = node.getAttribute("callsign")
				ip = node.getAttribute("server_ip")
				if servers_lookup.has_key(ip):
					server = servers_lookup[ip]
				else:
					server = ip
				dic = {
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

				callsign = node.getAttribute("callsign")
				if callsign.startswith("atc"):
					atc[callsign] = dic
				else:
					pilots[callsign] = dic
			#print player_ips
			#servers = server_ips()
			for server in player_ips:
				if not memcache.set("server_count_%s" % server, player_ips[server]):
					print "fail"
			


			## callsigns
			callsigns =  sorted(pilots.keys())
			if not memcache.set("callsigns", callsigns):
				print "error"

			## info 
			info = {'pilots_count': len(pilots), 
					'atc_count': len(atc),
					'updated': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			}
			if not memcache.set("pilots_info", info):
				print "error"

			pilots_sorted = []
			for ki in callsigns:
				pilots_sorted.append( pilots[ki] )
			if not memcache.set("pilots_online", pilots_sorted):
				print "error"

			if not memcache.set("atc_online", atc):
				print "error"
			return info



####################################################
## MP Server Queries
####################################################
def mp_servers():
	#data = memcache.get("mp_servers")
	#if data is not None:
	#	return data
	query = db.GqlQuery("SELECT * FROM MPServer order by no asc")
	servers = query.fetch(100)
	reply = []
	for server in servers:
		dic = {	'no': server.no, 
				'name': server.name, 
				'location': server.location , 
				'status': server.status, 
				'status_updated': server.status_updated.strftime("%Y-%m-%d %H:%M:%S") if server.status_updated else None,
				'port': server.port,
				'host': server.host, 
				'ip': server.ip
		}
		reply.append(dic)
	return reply


def mp_servers_info():
	return	memcache.get("mpservers_info")

def server_ip_lookup():
	servers = mp_servers()
	ret = {}
	local = ''
	for server in servers:
		ret[server.ip] = server.server
		if server.server == "mpserver02":
			ret['LOCAL'] = server.name
		else:
			ret[server.ip] = server.name
	return ret

####################################################
## MP Servers Update
####################################################
def mpservers_status_update():
	""" Parses out the http://mpmap01.flightgear.org/mpstatus/ page """
	## fetch content 
	try:
		result = urlfetch.fetch(conf.MP_STATUS_URL)
	except:#
		return False
	if result.status_code == 200:
		#print result.content	
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
				
		mpservers_info = {'updated': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
				'up': up, 'down': down, 'total': up + down
		}
		memcache.set("mpservers_info", mpservers_info)
		return mpservers_info

