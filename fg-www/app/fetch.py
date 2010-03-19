# -*- coding: utf-8 -*-

import datetime
import random

from google.appengine.ext import db
from google.appengine.api import memcache


from django.utils import simplejson as json
from libs.BeautifulSoup import BeautifulSoup 
from google.appengine.api import urlfetch
import xml.dom.minidom

import gdata.youtube.service
import gdata.gauth
import gdata.client
import gdata.data
import atom.http_core
import atom.core


import conf


####################################################
## Pilots Online
####################################################
def pilots_online():
	if 1 == 0:
		data = memcache.get("pilots_online")
		if data is not None:
			return data
	return get_pilots_feed()

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
					'updated': datetime.datetime.now()
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
			return pilots_sorted


####################################################
## Git 
####################################################
def git_feed(git):
	
	json_str = memcache.get('git_feed', namespace=git)
	if json_str:
		return json.loads(json_str)

	if git == 'gitorious':
		url = 'http://gitorious.org/fg/flightgear.atom'
	else:
		url = "http://pigeond.net/git/?a=atom;p=%s;" % git
	result = urlfetch.fetch(url) 
	if result.status_code == 200:
		xml_str = result.content
	else:
		pass # TODO
		return None
	entries = BeautifulSoup.BeautifulSoup(xml_str).findAll("entry")
	records = []
	for entry in entries:
		updated = entry.updated.text.replace("T", " ").replace("Z","").replace("/", "-")
		rec = {	'author': entry.author.findAll("name")[0].text
				, 'title': entry.title.text
				, 'content': entry.content.text
				, 'updated': updated
		}
		records.append(rec)
	if not memcache.set("git_feed", json.dumps(records), 60, namespace=git):
		pass # TODO
	return records

def git_feeds():

	#json_str = memcache.get("git_feed")
	#if json_str:
		#return json.loads(json_str)
	url = "http://pigeond.net/git/?p=flightgear/flightgear.data.git&a=search&h=HEAD&st=commit&s=787"
	result = urlfetch.fetch(url) #conf.GIT_ATOM)
	if result.status_code == 200:
		xml_str = result.content
	else:
		pass # TODO
		return None
	#table = BeautifulSoup.BeautifulSoup(xml_str).findAll("table")
	html_rows = BeautifulSoup.BeautifulSoup(xml_str).findAll("tr")
	return_rows = []
	for html_row in html_rows:
		#print html_row
		cells = html_row.findAll("td")
		if len(cells) == 4:
			row = {}
			row['len'] = len(cells)
			row['updated'] = cells[0].text
			row['author'] = cells[1].text
			row['title'] = cells[2].text
			#print "\n##########", row, "\n"
			return_rows.append(row)
	return return_rows

####################################################
## MP Server Queries
####################################################
def mp_servers():
	return
	data = memcache.get("mp_servers")
	if data is not None:
		return data
	query = db.GqlQuery("SELECT * FROM MPServer order by no asc")
	data = query.fetch(100)
	if not memcache.set("mp_servers", data, 120):
		print "error"
	return data

def mp_servers_info():
	mp_servers_info =	memcache.get("mp_servers_info", namespace="mp_servers")
	if mp_servers_info:
		return mp_servers_info['servers_info']
	try:
		result = urlfetch.fetch("http://fg-online.appspot.com/feed/servers/info/")
	except:
		return False
	if result.status_code == 200:
		mp_servers_info = json.loads(result.content)
		memcache.set("mp_servers_info", mp_servers_info, (60), namespace="mp_servers")
		return mp_servers_info['servers_info']

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

####################################################
## MP Servers Update
####################################################
def mpservers_status_update():
	""" Parses out the http://mpmap01.flightgear.org/mpstatus/ page """

	## fetch content 
	try:
		result = urlfetch.fetch(conf.MP_STATUS_URL)
	except:
		return False
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



#######################################################
## Gallery
#######################################################
def gallery():
	gallery = memcache.get("gallery", namespace="gallery")
	if gallery:
		return gallery
	result = urlfetch.fetch("http://flightgear-gallery.googlecode.com/svn/trunk/gallery.js")
	if result.status_code == 200:
		gallery_dic = json.loads(result.content)
		gallery = gallery_dic['gallery']
		if not memcache.set("gallery", gallery, (60 * 60), namespace="gallery"): # every hour
			print "error" #TODO
	return gallery

def gallery_random():
	return random.choice( gallery() )


#######################################################
## Liveries
#######################################################
def liveries():
	return fetch_liveries()
	liveries =	memcache.get("liveries")
	if liveries:
		return liveries
	liveries =  fetch_liveries()
	if not memcache.set("liveries", liveries, 240):
		print "error"
	return liveries

def fetch_liveries():
	result = urlfetch.fetch("http://liveries.flightgear.org/rss.php")
	if result.status_code == 200:
		#print result.content
		entries = BeautifulSoup.BeautifulSoup(result.content).findAll("item")
		records = []
		for entry in entries:
			##TODO - link not work ??
			rec = {	'author': entry.author.text
					, 'title': entry.title.text
					, 'link': entry.link.text
			}
			#print entry
			records.append(rec)
		if not memcache.set("liveries", json.dumps(records), 60):
			pass # TODO
		return records
	else:
		return None

#######################################################
## Mailing List latest Topics # TODO
#######################################################
def mailing_list(self, list_address):
	return fetch_mailing_list(list_address)
	maillist =	memcache.get(list_address, namespace="maillist")
	if maillist:
		return maillist
	maillist =  fetch_liveries()
	if not memcache.set("maillist", maillist, 240):
		print "error"
	return liveries

def fetch_mailing_list(self, list_address):
	
	url ="http://www.mail-archive.com/%s/maillist.xml" % list_address
	print list_address, url
	result = urlfetch.fetch(url)
	print result.content
	if result.status_code == 200:
		print result.content
		entries = BeautifulSoup.BeautifulSoup(result.content).findAll("item")
		records = []
		for entry in entries:
			##TODO - link not work ??
			rec = {	'author': entry.author.text
					, 'title': entry.title.text
					, 'link': entry.link.text
			}
			#print entry
			records.append(rec)
		if not memcache.set("liveries", json.dumps(records), 60, namespace="maillist"):
			pass # TODO
		return records
	else:
		return None

#######################################################
## Versions
#######################################################
def versions():
	versions =	memcache.get("versions")
	if versions:
		return versions
	versions =  fetch_versions()
	if not memcache.set("versions", versions, 240):
		print "error"
	return versions

def fetch_versions():
	## fetch content 
	result = urlfetch.fetch("http://www.flightgear.org/version.html")
	if result.status_code == 200:
			
		soup = BeautifulSoup.BeautifulSoup(result.content)
		table = soup.findAll('table')[1]
		cell = table.findAll("td")[0]
		#lines = cell.split("\n")
		lines = str(cell).split("\n")
		in_h3 = False
		versions = []
		info = ''
		h3 = None
		for line in lines:
			#print "#", line
			if line.upper().startswith("<H3"):
				if h3:
					versions.append({'version': h3.strip(), 'info': info})
					info = ''
				in_h3 = True
				h3 = BeautifulSoup.BeautifulSoup(line).text
				#print "H3=", h3
				curr_ver = h3
			elif in_h3:
				info += line
		#print "############", versions
		return versions



#######################################################
## Videos
#######################################################
def videos( filter_str="", max_results=10):
	videos = memcache.get(filter_str, namespace="videos")
	if videos:
		return videos
	videos =  fetch_videos(filter_str, max_results)
	if not memcache.set("videos", videos, 300, namespace="videos"):
		print "error"
	return videos

def fetch_videos(filter_str, max_results):
	query_str = filter_str
	client = gdata.youtube.service.YouTubeService()
	query = gdata.youtube.service.YouTubeVideoQuery()
	query.vq = query_str
	query.max_results = max_results
	#query.order_by = "rating"
	feed = client.YouTubeQuery(query)	
	#print feed
	videos = []
	for entry in feed.entry:
		v = process_vid_entry(entry)
		videos.append(v)
	return videos

def process_vid_entry( entry):
	dic = {}
	dic['id'] = entry.id.text.split("/")[-1]
	dic['title'] = entry.title.text
	dic['thumbnail'] = entry.media.thumbnail[0].url
	return dic
