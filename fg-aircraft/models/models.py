# -*- coding: utf-8 -*-
from google.appengine.ext import db

class Developer(db.Model):
	cvs = db.StringProperty()
	name = db.StringProperty()
	

class Aero(db.Model):
	aero = db.StringProperty()
	directory =  db.StringProperty()
	description = db.StringProperty()
	splash = db.StringProperty()
	fdm = db.StringProperty()
	status = db.StringProperty()
	version = db.StringProperty()
	last_updated = db.DateTimeProperty()
	author = db.StringProperty()
	cvs_users = db.StringListProperty()
	
"""
[{"file": {"head": " 1.1", "file": " 14bis-base.xml", "rcs": " /var/cvs/FlightGear-0.9/data/Aircraft/14bis/14bis-base.xml,v"}, "revision": {"date": "2008/09/22 23:08:47", "state": "Exp", "revision": "1.1", "message": "- new plane", "author": "helijah"}},

lambda x: datetime.datetime.strptime(x, '%m/%d/%Y').date()),
"""
class AeroFile(db.Model):
	file_name = db.StringProperty(indexed=True)
	directory = db.StringProperty(indexed=True)
	head = db.StringProperty()
	rcs = db.StringProperty()
	revision = db.StringProperty()
	last_update = db.DateTimeProperty(indexed=True)
	
class Revision(db.Model):
	aero_file = db.ReferenceProperty(AeroFile)
	dev = db.ReferenceProperty(Developer)
	message = db.TextProperty()
	revision = db.StringProperty(indexed=True)
	dated = db.DateTimeProperty()
	

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


class AeroLog(db.Model):
	aero = db.ReferenceProperty(Aero)
	dated = db.DateTimeProperty(auto_now_add=True)
	log = db.StringProperty(multiline=True)
	