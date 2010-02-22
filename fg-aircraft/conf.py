# -*- coding: utf-8 -*-

#FEED = "http://code.google.com/feeds/issues/p/flightgear-bugs/issues/full"

PROJECT_NAME = "flightgear-bugs"
ISSUES_FEED = 'http://code.google.com/feeds/issues/p/flightgear-bugs/issues/full'

USER_NAME = 'flightgear.bot@googlemail.com'
USER_PASS = 'daffo0217'

MP_STATUS_URL = "http://mpmap01.flightgear.org/mpstatus/"
MP_PILOTS_URL = "http://mpmap02.flightgear.org/fg_server_xml.cgi?mpserver02.flightgear.org:5001"


nav = []
nav.append( {'path':'/', 'label': 'Home'} )
nav.append( {'path':'/aircraft/', 'label': 'Aircraft'} )
nav.append( {'path':'/online/', 'label': 'Pilots Online'} )
nav.append( {'path':'/mpservers/', 'label': 'MP Servers'} )
nav.append( {'path':'/mapservers/', 'label': 'Map Servers'} )
#nav.append( {'path':'/developers/', 'label': 'Developers'} )
nav.append( {'path':'/issues/', 'label': 'Issues'} )
nav.append( {'path':'/source/', 'label': 'Source'} )

import app.fetch

app_vars = { 
			'pilots_count': app.fetch.pilots_count(),
			'servers_up': app.fetch.servers_up(),
			'servers_down': app.fetch.servers_down()
}

