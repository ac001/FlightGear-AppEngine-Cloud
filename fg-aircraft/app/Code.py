# -*- coding: utf-8 -*-
import os
from django.utils import simplejson as json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import memcache
from google.appengine.ext import db

from google.appengine.api import urlfetch
import datetime

import conf
import app.fetch
from models.models import Developer



class CodePage(webapp.RequestHandler):

	def get(self, action=None):

		subtabs = []
		subtabs.append({'label': 'FlightGear Source', 'page': 'flightgear/flightgear.source.git'})
		subtabs.append({'label': 'SimGear Source', 'page': 'flightgear/simgear.git'})
		subtabs.append({'label': 'FlightGear Data', 'page': 'flightgear/flightgear.data.git'})
		subtabs.append({'label': 'Gitorious', 'page': 'gitorious'})

		page = self.request.get("page")
		if not page:
			page = subtabs[0]['page']

		template_values = {
			'conf': conf, 'path': "code/", 'title': 'Code',  "page": page,
			'git': app.fetch.git_feed(page),
			'subtabs': subtabs
		}

		path = os.path.join(os.path.dirname(__file__), 'templates/code.html')
		self.response.out.write(template.render(path, template_values))
