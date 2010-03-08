# -*- coding: utf-8 -*-

APP_ID = 'fg-master'

tm = "<span class='tm'>FlightGear&#0174;</span>"

SITE_TITLE = "FlightGear Master Machine"
SITE_HEADER = 'Master Machine'

GOOGLE_PROJECT = "flightgear-bugs"
ISSUES_FEED = 'http://code.google.com/feeds/issues/p/flightgear-bugs/issues/full'

USER_NAME = 'flightgear.bot@googlemail.com'
USER_PASS = 'daffo0217'

MP_STATUS_URL = "http://mpmap01.flightgear.org/mpstatus/"
MP_PILOTS_URL = "http://mpmap02.flightgear.org/fg_server_xml.cgi?mpserver02.flightgear.org:5001"

GIT_ATOM = "http://pigeond.net/git/?p=flightgear/flightgear.data.git;a=atom"

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
