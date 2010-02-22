# -*- coding: utf-8 -*-
import os
from django.utils import simplejson as json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import memcache
from google.appengine.ext import db

from google.appengine.api import urlfetch
import xml.dom.minidom

from models.models import Aero

class FeedsPage(webapp.RequestHandler):

	def get(self):
		
		

		template_values = {
			'title': 'Aircraft', 'aero': None
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/feed-viewer.html')
		self.response.out.write(template.render(path, template_values))




