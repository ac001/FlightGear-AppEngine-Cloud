# -*- coding: utf-8 -*-
from google.appengine.ext import db

class MPServer(db.Model):
	no = db.IntegerProperty()
	name = db.StringProperty(indexed=True)
	host= db.StringProperty()
	port = db.IntegerProperty()
	ip = db.StringProperty(indexed=True)
	dev = db.IntegerProperty()
	location = db.StringProperty()
	maintainer = db.StringProperty()
	updated = db.DateTimeProperty()
	status = db.StringProperty()
	status_updated = db.DateTimeProperty()
	

class MPServerLog(db.Model):
	server = db.ReferenceProperty(MPServer)
	dated = db.DateTimeProperty(auto_now_add=True, indexed=True)
	log = db.StringProperty(multiline=True)