# -*- coding: utf-8 -*-

import datetime
import random

from google.appengine.ext import db
from google.appengine.api import memcache


from django.utils import simplejson as json
#from BeautifulSoup import BeautifulSoup 
from google.appengine.api import urlfetch
#import xml.dom.minidom
"""
import gdata.projecthosting.client
import gdata.projecthosting.data
import gdata.gauth
import gdata.client
import gdata.data
import atom.http_core
import atom.core
"""
import conf
#from models.models import MPServer


"""
This is the main "Object" that is passed to the template

A "function_call()" appears as "app.function_call"

Its a pain in the ass that within a tempalte app.function_call("argument_with_django")
is not allowed

"""

## Import main Calls
import app.fetch

##############################################################
## App Calls Class
##############################################################
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
							{'path':'/index/setup/', 'label': 'Fly Multiplayer'},
							{'path':'/index/setup/', 'label': 'Voice Setup'},
							{'path':'/index/mpserver/', 'label': 'MP Server'},
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
