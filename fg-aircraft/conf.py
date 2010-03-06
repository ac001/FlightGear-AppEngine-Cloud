# -*- coding: utf-8 -*-

import app.fetch

#FEED = "http://code.google.com/feeds/issues/p/flightgear-bugs/issues/full"

SITE_TITLE = "FlightGear GAE Cloud Experiment"

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


app_vars = { 'foo': 'bar',
			'pilots_info': app.fetch.pilots_info(),
			'mpservers_info': app.fetch.mpservers_info()
}



tm = "<span class='tm'>FlightGear</span>"

platforms = [	{'platform': 'windows', 'label': 'Windows'},
				{'platform': 'linux', 'label': 'Linux'},
				{'platform': 'mac', 'label': 'Mac OSX'},
				{'platform': 'freebsd', 'label': 'Free BSD'},
				{'platform': 'sgi', 'label': 'SGI'}
]

front_nav = []
front_nav.append( {'path':'/idea/', 'label': 'Home', 
				'subnav': [	
					{'path':'/idea/home/announce/', 'label': 'Announcements'},
					{'path':'/idea/home/calendar/', 'label': 'Calendar'},
				]
})
front_nav.append( {'path':'/idea/about/', 'label': 'About', 
				'subnav': [	
					{'path':'/idea/about/features/', 'label': 'Features'},
					{'path':'/idea/about/license/', 'label': 'License'}
				]
})
#nav.append( {'path':'/idea/features/', 'label': 'Features'} )

front_nav.append( {'path':'/idea/download/', 'label': 'Download',
			'subnav': [	
				{'path':'/idea/download/requirements/', 'label': 'Requirements'}, 	
				{'path':'/idea/download/flightgear/', 'label': 'FlightGear'}, 	
				#{'path':'/idea/download/aircraft/', 'label': 'Aircraft'},
				{'path':'/idea/download/scenery/', 'label': 'Scenery'},
				{'path':'/idea/download/versions/', 'label': 'ChangeLog'},
			]
})
front_nav.append( {'path':'/idea/support/', 'label': 'Support', 
				'subnav': [	
					{'path':'/idea/support/docs/', 'label': 'Documentation'},
					{'path':'/idea/support/faq/', 'label': 'FAQ'}
				]
})

front_nav.append( {'path':'/idea/gallery/', 'label': 'Gallery'} )
#front_nav.append( {'path':'/mpservers/', 'label': 'Aircraft'} )
#nav.append( {'path':'/mapservers/', 'label': 'Map Servers'} )
#nav.append( {'path':'/developers/', 'label': 'Developers'} )
front_nav.append( {'path':'/idea/multiplayer/', 'label': 'Multi Player'
, 			'subnav': [	
					{'path':'/idea/multiplayer/servers/', 'label': 'Servers'},
					{'path':'/idea/multiplayer/pilots/', 'label': 'Pilots Online'},
					{'path':'/idea/multiplayer/atc/', 'label': 'ATC Online'},
					{'path':'/idea/multiplayer/map/', 'label': 'Online Map'}
			]
})
front_nav.append( {'path':'/developers/', 'label': 'Links'} )
front_nav.append( {'path':'/code/', 'label': 'Developers'} )

langs = [ 	{'code': 'En', 'label': 'English'},
			{'code': 'Fi', 'label': 'French'},
			{'code': 'Es', 'label': 'Spanish'},
			{'code': 'De', 'label': 'German'}
]

