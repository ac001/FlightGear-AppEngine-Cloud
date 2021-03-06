# -*- coding: utf-8 -*-

APP_ID = 'fg-online'

tm = "<span class='tm'>FlightGear&#0174;</span>"

SITE_TITLE = "FlightGear Cloud Experiment"
SITE_HEADER = "Online Multi Player"


MP_STATUS_URL = "http://mpmap01.flightgear.org/mpstatus/"
MP_PILOTS_URL = "http://mpmap02.flightgear.org/fg_server_xml.cgi?mpserver02.flightgear.org:5001"

##########################################################
## Langs - TODO add links
##########################################################
langs = [ 	{'code': 'En', 'label': 'English'},
			{'code': 'Fi', 'label': 'French'},
			{'code': 'Es', 'label': 'Spanish'},
			{'code': 'De', 'label': 'German'}
]


sites_nav = [ 
	{'url': 'http://fg-www.appspot.com', 'label': 'Website', 'id': 'fg-www'},
	{'url': 'http://fg-aircraft.appspot.com', 'label': 'Aircraft', 'id': 'fg-aircraft'},
	{'url': 'http://fg-online.appspot.com', 'label': 'Online', 'id': 'fg-online'},
	{'url': 'http://wiki.flightgear.org', 'label': 'Wiki', 'id': 'wiki'},
	{'url': 'http://www.flightgear.org/forums/', 'label': 'Forums', 'id': 'forums'}
]