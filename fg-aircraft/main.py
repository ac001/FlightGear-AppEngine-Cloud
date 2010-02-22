# -*- coding: utf-8 -*-

import os
import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import app.Index
import app.PilotsOnline
import app.MPServers
import app.Aircraft
import app.Aero
import app.Feeds
import app.Issues



# 										('/cron/pilots_online', app.PilotsOnline.PilotsOnlineCron),

application = webapp.WSGIApplication([	('/', app.Index.Index),
										('/pilots_online/', app.PilotsOnline.PilotsOnline),
										#('/rpc/pilots_online', app.PilotsOnline.PilotsOnlineRpc),

										('/mpservers/', app.MPServers.MPServers),
										('/rpc/mpservers', app.MPServers.MPServersRpc),

										('/aircraft/', app.Aircraft.AircraftPage),
		
										('/rpc/aircraft', app.Aircraft.AircraftRpc),

										('/feeds', app.Feeds.FeedsPage),

										('/aero/(.*)/', app.Aero.AeroPage),
										('/issues/', app.Issues.IssuesPage),
									],
									debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()