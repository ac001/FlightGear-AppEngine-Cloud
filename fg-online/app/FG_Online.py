# -*- coding: utf-8 -*-

import datetime
import random

from google.appengine.ext import db
from google.appengine.api import memcache


from django.utils import simplejson as json
#from BeautifulSoup import BeautifulSoup 
from google.appengine.api import urlfetch
#import xml.dom.minidom

import conf

import app.fetch


class FG_Online:


	def mp_servers(self):
		return app.fetch.mp_servers()

	def mp_servers_json_feed(self):
		
		reply = {}

		servers = app.fetch.mp_servers()
		reply['servers'] = []
		for server in servers:
			dic = {	'no': server.no, 
					'server': server.server, 
					'location': server.location , 
					'status': server.status, 
					'status_updated': server.status_updated,
					'port': server.port,
 					'host': server.host, 
					'ip': server.ip
			}
			reply['servers'].append(dic)
		return reply




	def sites_nav(self):
		return [ 
			{'url': 'http://fg-www.appspot.com', 'label': 'www', 'id': 'fg-www'},
			{'url': 'http://fg-aircraft.appspot.com', 'label': 'Aircraft', 'id': 'fg-aircraft'},
			{'url': 'http://fg-online.appspot.com', 'label': 'Online', 'id': 'fg-online'},
			{'url': 'http://wiki.flightgear.org', 'label': 'Wiki', 'id': 'wiki'},
			{'url': 'http://www.flightgear.org/forums/', 'label': 'Forums', 'id': 'forums'}
		]
	
	def nav(self):
		"""Return navigation - used in tempalte """
		return self._nav

	

	def title(self, path):
		"""Return the title or label from path based lookup"""
		if path in self._paths:
			if 'title' in self._paths[path]:
				return  self._paths[path]['title']
			else:
				return  self._paths[path]['label']
		return "#### NO TITLE ###"


	def nav_append(self, dic):
		"""Append items to navigations"""
		self._nav.append(dic)
		self._paths[dic['path']] = dic
		if 'subnav' in dic:
			for subpage in dic['subnav']:
				self._paths[subpage['path']] = subpage



	def __init__(self):
		"""Initialise Navigation and add navigations items"""
		### TODO authenticated sections


		self._nav = []
		self._paths = {}

		self.nav_append( {'path':'/index/', 'label': 'Online Multi Player'
		, 			'subnav': [	
							{'path':'/index/setup/', 'label': 'Aircraft Setup'},
							{'path':'/index/fgcom/', 'label': 'Voice Setup'},
							{'path':'/index/server_setup/', 'label': 'Create Server'},
					]
		})
		
		self.nav_append( {'path':'/pilots/', 'label': 'Pilots Flying'
		})
		self.nav_append( {'path':'/atc/', 'label': 'ATC'
		})
		"""
		self.nav_append( {'path':'/', 'label': 'Online Multi Player'
		, 			'subnav': [	
							{'path':'/servers/', 'label': 'Servers'},
							{'path':'/pilots/', 'label': 'Pilots'},
							{'path':'/atc/', 'label': 'ATC'},
							{'path':'/map/', 'label': 'Online Map'}
					]
		})
		"""
		servers = self.mp_servers()
		servers_list = []
		for server in self.mp_servers():
			servers_list.append({	'path': '/servers/%s/' % server.server,
									'label': server.server
								})
		self.nav_append( {'path':'/servers/', 'label': 'Servers', 'subnav': servers_list})
