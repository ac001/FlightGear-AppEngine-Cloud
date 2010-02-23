# -*- coding: utf-8 -*-

import os
import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import app.Index
import app.Online
import app.MPServers
import app.Aircraft
import app.Aero
import app.Feeds
import app.Issues
import app.Devs

# 										('/cron/pilots_online', app.PilotsOnline.PilotsOnlineCron),

application = webapp.WSGIApplication([	('/', app.Index.Index),
										('/online/', app.Online.OnlinePage),
										#('/online/', app.Online.Online),
										#('/rpc/pilots_online', app.PilotsOnline.PilotsOnlineRpc),

										('/mpservers/', app.MPServers.MPServersPage),
										('/mpservers/import/', app.MPServers.MPServerImport),
										('/mpservers/update/', app.MPServers.MPServersUpdateStatus),
										('/mpserver/(.*)/', app.MPServers.MPServerPage),
										('/rpc/mpservers', app.MPServers.MPServersRpc),

										('/aircraft/', app.Aircraft.AircraftPage),
										('/aircraft/(.*)/', app.Aircraft.AircraftPage),
										('/rpc/aircraft/', app.Aircraft.AircraftRpc),		

										('/import/aircraft/', app.Aircraft.AircraftImport),
										('/import/revisions/', app.Aircraft.AircraftImportRevisions),

										('/feeds', app.Feeds.FeedsPage),
										('/developers/', app.Devs.DevsPage),

										#('/aero/(.*)/', app.Aero.AeroPage),
										('/issues/', app.Issues.IssuesPage),
									],
									debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()