# -*- coding: utf-8 -*-
from google.appengine.ext import db

class MPServer(db.Model):
	no = db.StringProperty()
	server = db.StringProperty(indexed=True)
	description = db.StringProperty()
	host= db.StringProperty()
	port = db.StringProperty()
	ip = db.StringProperty()
	dev = db.BooleanProperty()
	location = db.StringProperty()
	status = db.StringProperty()
	status_updated = db.DateTimeProperty()

