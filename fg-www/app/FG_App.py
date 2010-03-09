# -*- coding: utf-8 -*-

import datetime
import random

from google.appengine.ext import db
from google.appengine.api import memcache

from django.utils import simplejson as json
from google.appengine.api import urlfetch


import conf
import app.fetch

##############################################################
## App Calls Class
##############################################################
class FG_App:

	def liveries(self):
		return app.fetch.liveries()

	def versions(self):
		return app.fetch.versions()

	## Mailing Lists
	def devel_mailing_list(self):
		return mailing_list('flightgear-devel@lists.sourceforge.net')
	def users_mailing_list(self):
		return mailing_list('flightgear-users@lists.sourceforge.net')

	def mp_servers(self):
		return app.fetch.mp_servers()

	### Videos
	def video_tutorials(self):
		return  app.fetch.videos('+FlightGear +tutorial')
	def video_howtos(self):
		return  app.fetch.videos('+flightgear +howto')
	
	### Forums
	def forums_list(self):
		return  [ 
			{'key': 'general', 'id': 2, 'title': 'General Help'},
			{'key': 'install', 'id': 11,'title': 'Install Help'},
			{'key': 'events', 'id': 10, 'title':'Events'},
			{'key': 'aircraft', 'id': 4, 'title':'Aircraft Development'},
			{'key': 'scenery', 'id': 5, 'title':'Scenery Enancment'},
			{'key': 'stories', 'id': 3, 'title':'Stories and Humour'},
			{'key': 'new_features', 'id': 6, 'title':'New Features'}
		]

	### Irc Channels
	def irc_channels(self):
		return [ 
			{'channel': 'flightgear', 'title': 'Main Channel'},
			{'channel': 'fg_cantene', 'title': 'Pilots Mess' },
			{'channel': 'fg_school', 'title': 'Flight Training' },
			{'channel': 'airliners', 'title': 'flightgear'},
			{'channel': 'wiki', 'title': 'Wiki Chat' }
		]
	

	## Gallery
	def gallery(self):
		return app.fetch.gallery_thumbs()

	def random_image(self):
		return app.fetch.gallery_random()

	
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

		self.nav_append( {'path':'/index/', 'label': 'Index', 'title': 'Welcome',
						'subnav': [	
							{'path':'/index/announce/', 'label': 'Announcements', 'title': 'News and announcments'},
							{'path':'/index/calendar/', 'label': 'Calendar', 'title': 'Calendar'},
						]
		})

		self.nav_append( {'path':'/about/', 'label': 'About', 'title': 'About FlightGear',
						'subnav': [	
							{'path':'/about/features/', 'label': 'Features' },
							{'path':'/about/license/', 'label': 'License'}
						]
		})
		self.nav_append( {'path':'/media/', 'label': 'Media', 
						'subnav': [	
							{'path':'/media/videos/', 'label': 'Videos', 'title': 'Videos'},
							{'path':'/media/gallery/', 'label': 'Image Gallery'}
						]
		})
		self.nav_append( {'path':'/support/', 'label': 'Support', 
						'subnav': [	
							{'path':'/support/docs/', 'label': 'Documentation'},
							{'path':'/support/faq/', 'label': 'FAQ', 'title': 'Frequently Answered Questions'}
						]
		})
		self.nav_append( {'path':'/download/', 'label': 'Download', 'title': 'Download Central',
					'subnav': [	
						{'path':'/download/requirements/', 'label': 'Requirements', 'title': 'Hardware Requirements'}, 	
						{'path':'/download/flightgear/', 'label': 'FlightGear', 'title': 'Download FlightGear'}, 	
						#{'path':'/download/aircraft/', 'label': 'Aircraft'},
						{'path':'/download/scenery/', 'label': 'Scenery'},
						{'path':'/download/versions/', 'label': 'Versions', 'title': 'Version Summary'},
					]
		})
		#nav.append( {'path':'/features/', 'label': 'Features'} )
		#self.nav_append( {'path':'/aircraft/', 'label': 'Aircraft'} )
		#self.nav_append( {'path':'/multiplayer/', 'label': 'Online Multi Player' })
		"""
		, 			'subnav': [	
							{'path':'/multiplayer/servers/', 'label': 'Servers'},
							{'path':'/multiplayer/pilots/', 'label': 'Pilots'},
							{'path':'/multiplayer/atc/', 'label': 'ATC'},
							{'path':'/multiplayer/map/', 'label': 'Online Map'}
					]
		})
		"""
		#self.nav_append( {'path':'/mpservers/', 'label': 'Aircraft'} )
		#nav.append( {'path':'/mapservers/', 'label': 'Map Servers'} )
		#nav.append( {'path':'/developers/', 'label': 'Developers'} )


		self.nav_append( {'path':'/developers/', 'label': 'Developers',
					'subnav': [	
							{'path':'/developers/src/', 'label': 'Source Code'},
							{'path':'/developers/credits/', 'label': 'Credits'}
					]
		})
		self.nav_append( {'path':'/links/', 'label': 'Links',
					'subnav': [	
							{'path':'/links/sites/', 'label': 'Related Sites'},
							{'path':'/links/projects/', 'label': 'Projects'}
					]
		})

## << class FG_Nav
