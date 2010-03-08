# -*- coding: utf-8 -*-

import os
import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
"""
import app.Index
import app.Online
import app.MPServers
import app.Aircraft

import app.Feeds
import app.Issues
import app.Devs
import app.Code
"""
import app.Rpc
import app.Handler
# 										('/cron/pilots_online', app.PilotsOnline.PilotsOnlineCron),

application = webapp.WSGIApplication([	('/', app.Handler.HandlerPage),
										('/rpc/(.*)/', app.Rpc.RpcHandler),
										('/(.*)/(.*)/', app.Handler.HandlerPage),
										('/(.*)/', app.Handler.HandlerPage),
										
									
									],
									debug=False)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()