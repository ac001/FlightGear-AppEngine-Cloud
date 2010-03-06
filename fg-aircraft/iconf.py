# -*- coding: utf-8 -*-

import app.fetch

#FEED = "http://code.google.com/feeds/issues/p/flightgear-bugs/issues/full"

SITE_TITLE = "FlightGear GAE Cloud Experiment"

"""
GOOGLE_PROJECT = "flightgear-bugs"
ISSUES_FEED = 'http://code.google.com/feeds/issues/p/flightgear-bugs/issues/full'

USER_NAME = 'flightgear.bot@googlemail.com'
USER_PASS = 'daffo0217'

MP_STATUS_URL = "http://mpmap01.flightgear.org/mpstatus/"
MP_PILOTS_URL = "http://mpmap02.flightgear.org/fg_server_xml.cgi?mpserver02.flightgear.org:5001"

GIT_ATOM = "http://pigeond.net/git/?p=flightgear/flightgear.data.git;a=atom"
"""

tm = "<span class='tm'>FlightGear</span>"

platforms = [	{'platform': 'windows', 'label': 'Windows'},
				{'platform': 'linux', 'label': 'Linux'},
				{'platform': 'mac', 'label': 'Mac OSX'},
				{'platform': 'freebsd', 'label': 'Free BSD'},
				{'platform': 'sgi', 'label': 'SGI'}
]

nav = []
nav.append( {'path':'/idea/', 'label': 'Home'} )
nav.append( {'path':'/idea/about/', 'label': 'About', 
				'subnav': [	
					{'path':'/idea/about/features/', 'label': 'Features'},
					{'path':'/idea/about/license/', 'label': 'License'}]
			})
#nav.append( {'path':'/idea/features/', 'label': 'Features'} )
nav.append( {'path':'/idea/news/', 'label': 'News'} )
nav.append( {'path':'/idea/download/', 'label': 'Download',
			'subnav': [	
				{'path':'flightgear/', 'label': 'FlightGear'}, 	
				{'path':'aircraft/', 'label': 'Aircraft'},
				{'path':'scenery/', 'label': 'Scenery'}
			]
})
nav.append( {'path':'/mpservers/', 'label': 'Aircraft'} )
#nav.append( {'path':'/mapservers/', 'label': 'Map Servers'} )
#nav.append( {'path':'/developers/', 'label': 'Developers'} )
nav.append( {'path':'/idea/multiplayer/', 'label': 'Multi Player'
, 			'subnav': [	
					{'path':'/idea/multiplayer/status/', 'label': 'Server Status'},
					{'path':'/idea/multiplayer/online/', 'label': 'Pilots Online'},
					{'path':'/idea/multiplayer/map/', 'label': 'Online Map'}
			]
})
nav.append( {'path':'/developers/', 'label': 'Links'} )
nav.append( {'path':'/code/', 'label': 'Developers'} )

langs = [ 	{'code': 'En', 'label': 'English'},
			{'code': 'Fi', 'label': 'French'},
			{'code': 'Es', 'label': 'Spanish'},
			{'code': 'De', 'label': 'German'}
]

app_vars = { 'foo': 'bar',
			'pilots_info': app.fetch.pilots_info(),
			'mpservers_info': app.fetch.mpservers_info()
}


"""
app_vars = { 'foo': 'bar',
			'pilots_info': app.fetch.pilots_info(),
			'mpservers_info': app.fetch.mpservers_info()
}
"""
