# -*- coding: utf-8 -*-



tm = "<span class='tm'>FlightGear&#0174;</span>"

SITE_TITLE = "FlightGear Cloud Experiment"

GOOGLE_PROJECT = "flightgear-bugs"
ISSUES_FEED = 'http://code.google.com/feeds/issues/p/flightgear-bugs/issues/full'

USER_NAME = 'flightgear.bot@googlemail.com'
USER_PASS = 'daffo0217'

MP_STATUS_URL = "http://mpmap01.flightgear.org/mpstatus/"
MP_PILOTS_URL = "http://mpmap02.flightgear.org/fg_server_xml.cgi?mpserver02.flightgear.org:5001"

GIT_ATOM = "http://pigeond.net/git/?p=flightgear/flightgear.data.git;a=atom"

"""
user = users.get_current_user()
if user:
	nickname = user.nickname()
	auth_url = users.create_logout_url("/")
else:
	nickname = None
	auth_url = users.create_login_url("/")

app_vars = { 'nickname': nickname, 'auth_url': auth_url,
			'pilots_info': app.fetch.pilots_info(),
			'mpservers_info': app.fetch.mpservers_info()
}
"""
"""
platforms = [	{'platform': 'windows', 'label': 'Windows'},
				{'platform': 'linux', 'label': 'Linux'},
				{'platform': 'mac', 'label': 'Mac OSX'},
				{'platform': 'freebsd', 'label': 'Free BSD'},
				{'platform': 'sgi', 'label': 'SGI'}
]
"""
###############################################################################
## Front Website Navigation
###############################################################################
front_nav = []
front_nav.append( {'path':'/', 'label': 'Index', 
				'subnav': [	
					{'path':'/index/announce/', 'label': 'Announcements'},
					{'path':'/index/calendar/', 'label': 'Calendar'},
				]
})

front_nav.append( {'path':'/about/', 'label': 'About', 
				'subnav': [	
					{'path':'/about/features/', 'label': 'Features'},
					{'path':'/about/license/', 'label': 'License'}
				]
})
front_nav.append( {'path':'/media/', 'label': 'Media', 
				'subnav': [	
					{'path':'/media/videos/', 'label': 'Videos'},
					{'path':'/media/gallery/', 'label': 'Image Gallery'}
				]
})
front_nav.append( {'path':'/support/', 'label': 'Support', 
				'subnav': [	
					{'path':'/support/docs/', 'label': 'Documentation'},
					{'path':'/support/faq/', 'label': 'FAQ'}
				]
})
front_nav.append( {'path':'/download/', 'label': 'Download',
			'subnav': [	
				{'path':'/download/requirements/', 'label': 'Requirements'}, 	
				{'path':'/download/flightgear/', 'label': 'FlightGear'}, 	
				#{'path':'/download/aircraft/', 'label': 'Aircraft'},
				{'path':'/download/scenery/', 'label': 'Scenery'},
				{'path':'/download/versions/', 'label': 'ChangeLog'},
			]
})
#nav.append( {'path':'/features/', 'label': 'Features'} )
front_nav.append( {'path':'/aircraft/', 'label': 'Aircraft'} )
front_nav.append( {'path':'/multiplayer/', 'label': 'Online Multi Player'
, 			'subnav': [	
					{'path':'/multiplayer/servers/', 'label': 'Servers'},
					{'path':'/multiplayer/pilots/', 'label': 'Pilots'},
					{'path':'/multiplayer/atc/', 'label': 'ATC'},
					{'path':'/multiplayer/map/', 'label': 'Online Map'}
			]
})






#front_nav.append( {'path':'/mpservers/', 'label': 'Aircraft'} )
#nav.append( {'path':'/mapservers/', 'label': 'Map Servers'} )
#nav.append( {'path':'/developers/', 'label': 'Developers'} )


front_nav.append( {'path':'/developers/', 'label': 'Developers',
			'subnav': [	
					{'path':'/developers/src/', 'label': 'Source Code'},
					{'path':'/developers/credits/', 'label': 'Credits'}
			]
})
front_nav.append( {'path':'/links/', 'label': 'Links',
			'subnav': [	
					{'path':'/links/sites/', 'label': 'Related Sites'},
					{'path':'/links/projects/', 'label': 'Projects'}
			]
})


##########################################################
## Langs - TODO add links
##########################################################
langs = [ 	{'code': 'En', 'label': 'English'},
			{'code': 'Fi', 'label': 'French'},
			{'code': 'Es', 'label': 'Spanish'},
			{'code': 'De', 'label': 'German'}
]





"""
download_servers = [
	{'location': 'Germany', 'server': 'ftp://ftp.de.flightgear.org/pub/fgfs/'},
	{'location': 'Germany', 'server': 'http://flightgear.mxchange.org/pub/fgfs/'},
	{'location': 'South Africa', 'server': '	 ftp://ftp.is.co.za/pub/games/flightgear/'},
	{'location': 'Ukraine', 'server': 'ftp://ftp.linux.kiev.ua/pub/mirrors/ftp.flightgear.org/flightgear/'},
	{'location': 'USA, North Carolina', 'server': 'ftp://mirrors.ibiblio.org/pub/mirrors/flightgear/ftp/'},
	{'location': 'USA, Minnesota', 'server': 'http://mirrors.ibiblio.org/pub/mirrors/flightgear/ftp/'},
	{'location': 'USA, California', 'server': 'ftp://ftp.kingmont.com/flightsims/flightgear/'}
]
"""
"""
## Done Import
if DownloadServer.all().count() == 0:
	for d in download_servers:
		ftp = DownloadServer()
		ftp.location = d['location']
		ftp.server = d['server']
		ftp.online = 1
		ftp.save()
"""
