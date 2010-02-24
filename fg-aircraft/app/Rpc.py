# -*- coding: utf-8 -*-

from django.utils import simplejson as json

from google.appengine.ext import webapp


import conf
import app.fetch


class RpcHandler(webapp.RequestHandler):
	def get(self, fetch):
		
		if fetch == "online":
			data = app.fetch.pilots_online()
		else:
			data = None

		payload = {'success': True, 'fetch': fetch, 'data': data}
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write(json.dumps(payload))