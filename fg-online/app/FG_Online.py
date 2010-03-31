# -*- coding: utf-8 -*-

import datetime
import random

from google.appengine.ext import db
from google.appengine.api import memcache


from django.utils import simplejson as json
from google.appengine.api import urlfetch

import conf
import app.fetch


class FG_Online:

	def mp_servers(self):
		return app.fetch.mp_servers()

	def sssmp_servers(self):
		
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

	def mp_servers_info(self):
		if self._mpservers_info == None:
			self._mpservers_info = app.fetch.mp_servers_info()
		return self._mpservers_info

	def pilots_info(self):
		return app.fetch.pilots_info()

	def pilots_online(self):
		return app.fetch.pilots_online()

	def atc_online(self):
		return app.fetch.atc_online()
	
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
		self._mpservers_info = None

		self._nav = []
		self._paths = {}

		self.nav_append( {'path':'/index/', 'label': 'About Multi Player'
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

		servers = self.mp_servers()
		servers_list = []
		for server in servers:
			servers_list.append({	'path': '/servers/%s/' % server['name'],
									'label': server['name']
								})
		self.nav_append( {'path':'/servers/', 'label': 'Servers', 'subnav': servers_list})

		self.nav_append( {'path':'/feeds/', 'label': 'Feeds'})
