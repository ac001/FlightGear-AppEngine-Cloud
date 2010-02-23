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



class DevsPage(webapp.RequestHandler):

	def get(self, action=None):
		query = Developer.all()
		devs = query.fetch(1000)
		template_values = {
			'conf': conf, 'path': self.request.path, 'title': 'Developers',
			'devs': devs
		}

		path = os.path.join(os.path.dirname(__file__), 'templates/developers.html')
		self.response.out.write(template.render(path, template_values))
