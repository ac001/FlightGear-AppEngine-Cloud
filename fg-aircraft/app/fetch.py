# -*- coding: utf-8 -*-

import datetime
import random

from google.appengine.ext import db
from google.appengine.api import memcache


from django.utils import simplejson as json
from BeautifulSoup import BeautifulSoup 
from google.appengine.api import urlfetch
import xml.dom.minidom

import gdata.projecthosting.client
import gdata.projecthosting.data
import gdata.gauth
import gdata.client
import gdata.data
import atom.http_core
import atom.core

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
	return info
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

####################################################
## MP Servers Update
####################################################
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


def TODOissues(aero=None):
	def all(self):
		"""Retrieve all the issues in a project."""
		#data = memcache.get("issues_all")
		#if data is not None:
		#	return data, True
		client = gdata.projecthosting.client.ProjectHostingClient()
		client.client_login(
					conf.USER_NAME,
					conf.USER_PASS,
					source='flightgear-bot',
					service='code')
		feed = client.get_issues(conf.GOOGLE_PROJECT)
		data = []
		print sfeed
		for issue in feed.entry:
			dic = process_entry(issue)
			data.append(dic)
		if not memcache.set("issues_all", data, 60):
			print "error"
		return data

def TODOprocess_issue_entry(issue):
	dic = {}
	dic['id'] = issue.id.text.split("/")[-1]
	dic['title'] = issue.title.text
	dic['labels'] = []
	for label in issue.label:
		dic['labels'].append(label.text)
	if issue.owner:
		#print issue.owner
		if issue.owner.username.text.find('@') > 0:
			dic['owner'] = issue.owner.username.text.split('@')[0]  #// take out email
		else:
			dic['owner'] = issue.owner.username.text
	
	dic['stars'] = issue.stars.text
	dic['state'] = issue.state.text
	dic['status'] = issue.status.text
	return dic

#######################################################
## Gallery
#######################################################
def gallery_thumbs():
	gallery =	memcache.get("gallery_thumbs")
	if gallery:
		return gallery
	gallery =  fetch_gallery_thumbs()
	if not memcache.set("gallery_thumbs", gallery, 240):
		print "error"
	return gallery

def fetch_gallery_thumbs():
	## fetch content 
	result = urlfetch.fetch("http://flightgear.org/Gallery-v2.0/thumbnails/")
	if result.status_code == 200:
			
		soup = BeautifulSoup.BeautifulSoup(result.content)
		links = soup.findAll('a')
		images = []
		for link in links:
			
			if link['href'].endswith(".jpg"):
				images.append(link['href'])
		return images #[0:5]

def gallery_random():
	gallery = gallery_thumbs()
	randy = random.choice(gallery)
	return randy


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

