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
import app.Rpc
import app.Feeds
import app.Issues
import app.Devs
import app.Code
"""
import app.Idea
# 										('/cron/pilots_online', app.PilotsOnline.PilotsOnl
application = webapp.WSGIApplication([	('/idea/', app.Idea.IdeaPage),
										('/idea/(.*)/(.*)/', app.Idea.LashUpSubPage),
										('/idea/(.*)/', app.Idea.LashUpPage),
										
									],
									debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()