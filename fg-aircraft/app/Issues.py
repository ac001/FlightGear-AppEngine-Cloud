# -*- coding: utf-8 -*-
import os
from django.utils import simplejson as json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import memcache

from google.appengine.api import urlfetch
import xml.dom.minidom

import gdata.projecthosting.client
import gdata.projecthosting.data
import gdata.gauth
import gdata.client
import gdata.data
import atom.http_core
import atom.core

import conf

class GoogleIssuesClient():

	def __init__(self):
		self.client = None
		self.login()

	def login(self):
		self.client = gdata.projecthosting.client.ProjectHostingClient()
		return self.client.client_login(
					conf.USER_NAME,
					conf.USER_PASS,
					source='flightgear-bot',
					service='code')

	def all(self):
		"""Retrieve all the issues in a project."""

		data = memcache.get("issues_all")
		if data is not None:
			return data, True

		feed = self.client.get_issues(conf.PROJECT_NAME)
		
		data = []
		for issue in feed.entry:
			#print issue.uri
			#print issue.username
			#print "------------------------------"
			dic = {}
			dic['labels'] = []
			for label in issue.label:
				dic['labels'].append(label.text)
			if issue.owner:
				#print issue.owner
				if issue.owner.username.text.find('@') > 0:
					dic['owner'] = issue.owner.username.text.split('@')[0]  #// take out email
				else:
					dic['owner'] = issue.owner.username.text
			dic['stars'] = issue.stars.text
			dic['state'] = issue.state.text
			dic['status'] = issue.status.text
			data.append(dic)
			#print dic
			if not memcache.set("issues_all", data, 10):
				print "error"
		return data, False


class IssuesPage(webapp.RequestHandler):


	def get(self):
		issuesObj = GoogleIssuesClient()
		issues, cached = issuesObj.all()
		#print self.request
		template_values = {
			'issues': issues, 'cached': cached, 
			'conf': conf, 'path': self.request.path
		}
		path = os.path.join(os.path.dirname(__file__), 'templates/issues.html')
		self.response.out.write(template.render(path, template_values))

