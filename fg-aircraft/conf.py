# -*- coding: utf-8 -*-

import app.fetch
from google.appengine.api import users
#from google.appengine.ext import db
#from models.models import DownloadServer
#FEED = "http://code.google.com/feeds/issues/p/flightgear-bugs/issues/full"

APP_ID = 'fg-aircraft'

tm = "<span class='tm'>FlightGear&#0174;</span>"

SITE_TITLE = "FlightGear Aircraft Cloud Experiment"
SITE_HEADER = "FlightGear Aircraft Database"

GOOGLE_PROJECT = "flightgear-bugs"
ISSUES_FEED = 'http://code.google.com/feeds/issues/p/flightgear-bugs/issues/full'

USER_NAME = 'flightgear.bot@googlemail.com'
USER_PASS = 'daffo0217'

MP_STATUS_URL = "http://mpmap01.flightgear.org/mpstatus/"
MP_PILOTS_URL = "http://mpmap02.flightgear.org/fg_server_xml.cgi?mpserver02.flightgear.org:5001"

GIT_ATOM = "http://pigeond.net/git/?p=flightgear/flightgear.data.git;a=atom"


nav = []
nav.append( {'path':'/', 'label': 'Home'} )
nav.append( {'path':'/aircraft/', 'label': 'Aircraft'} )
nav.append( {'path':'/online/', 'label': 'Pilots Online'} )
nav.append( {'path':'/mpservers/', 'label': 'MP Servers'} )
#nav.append( {'path':'/mapservers/', 'label': 'Map Servers'} )
#nav.append( {'path':'/developers/', 'label': 'Developers'} )
nav.append( {'path':'/issues/', 'label': 'Isssues'} )
nav.append( {'path':'/developers/', 'label': 'Developers'} )
nav.append( {'path':'/code/', 'label': 'Code'} )



sites_nav = [ 
	{'url': 'http://fg-www.appspot.com', 'label': 'Website', 'id': 'fg-www'},
	{'url': 'http://fg-aircraft.appspot.com', 'label': 'Aircraft', 'id': 'fg-aircraft'},
	{'url': 'http://fg-online.appspot.com', 'label': 'Online', 'id': 'fg-online'},
	{'url': 'http://wiki.flightgear.org', 'label': 'Wiki', 'id': 'wiki'},
	{'url': 'http://www.flightgear.org/forums/', 'label': 'Forums', 'id': 'forums'}
]




platforms = [	{'platform': 'windows', 'label': 'Windows'},
				{'platform': 'linux', 'label': 'Linux'},
				{'platform': 'mac', 'label': 'Mac OSX'},
				{'platform': 'freebsd', 'label': 'Free BSD'},
				{'platform': 'sgi', 'label': 'SGI'}
]

###############################################################################
## Front Website Navigation
###############################################################################
front_nav = []

front_nav.append( {'path':'/', 'label': 'Latest Updates'})

front_nav.append( {'path':'/aircraft/', 'label': 'Aircraft', 
				'subnav': [	
					{'path':'/aircraft/large_jets/', 'label': 'Large Jets'},
					{'path':'/aircraft/large_prop/', 'label': 'Large Props'},
					{'path':'/aircraft/small_jets/', 'label': 'Small Jets'},
					{'path':'/aircraft/small_prop/', 'label': 'Small Prop'},
					{'path':'/aircraft/small_prop/', 'label': 'Helicopters'},
				]
})
front_nav.append( {'path':'/livery/', 'label': 'Livery'})


front_nav.append( {'path':'/design/', 'label': 'Design',
			'subnav': [	
					{'path':'/idea/developers/src/', 'label': 'Basics'},
					{'path':'/idea/developers/credits/', 'label': 'Upload'}
			]
})





