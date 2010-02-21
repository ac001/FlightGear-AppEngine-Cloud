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


class MPServers(db.Model):
	server_id = db.StringProperty()
	long_name = db.StringProperty()
	host = db.StringProperty()
	port = db.StringProperty()
	ip = db.StringProperty()
	group = db.StringProperty()
	location = db.StringProperty()