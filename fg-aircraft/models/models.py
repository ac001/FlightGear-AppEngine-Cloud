# -*- coding: utf-8 -*-
from google.appengine.ext import db

class Aero(db.Model):
	aero = db.StringProperty()
	description = db.StringProperty()
	author = db.StringProperty()
	splash = db.StringProperty()
	fdm = db.StringProperty()
	status = db.StringProperty()
	version = db.StringProperty()


class MPServer(db.Model):
	no = db.StringProperty()
	server = db.StringProperty()
	description = db.StringProperty()
	host= db.StringProperty()
	port = db.StringProperty()
	ip = db.StringProperty()
	dev = db.BooleanProperty()
	location = db.StringProperty()
	status = db.StringProperty()
	status_updated = db.DateTimeProperty()


