#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Global Config uration for script execution

import os
import sys
import glob
import yaml

import urllib
import urllib2

import conf


if "--live" in sys.argv:
	WWW = "http://%s.appspot.com" % 'fg-online'
else:
	WWW = "http://localhost:8080"

## Ooen files from mpmap
content = open(conf.FG_MAP_ROOT + "/fgmap.servers").read()
lines = content.split("\n")


devel = False
for line in lines:
	line = line.strip()
	if line == "":
		#print "skip", line
		pass
	elif line.find("#") > -1:
		#print "skip", line
		pass
	elif line.find("--") > -1:
		if line.find("devel") > -1:
			devel = True
			print "tipped devel"
	else:
		#print "mp=", line
		parts = line.split("::")

		"""
		class MPServer(db.Model):
			no = db.StringProperty()
			name = db.StringProperty()
			description = db.StringProperty()
			host= db.StringProperty()
			port = db.StringProperty()
			ip = db.StringProperty()
			group = db.StringProperty()
			location = db.StringProperty()
		"""
		dic = {'dev': 1 if devel else 0}
		dic['no'] = parts[0].split(":")[0].replace("mpserver", "")
		dic['server'] = parts[0].split(":")[0]
		dic['description'] = parts[1]
		dic['host'] = parts[2]
		dic['port'] = parts[3]	
		dic['ip'] = parts[4]
		dic['location'] = parts[1].split(" ", 1)[1].replace("(", "").replace(")", "")
		#print dic
		
		#sys.exit(1)
		url = WWW + "/import/"
		if 1 == 1:
			data = urllib.urlencode(dic)
			#print url + "?" + data
			#print dic
			req = urllib2.Request(url + "?" + data) #, data)
			#req = urllib2.Request(url, data)
			response = urllib2.urlopen(req)
			the_page = response.read()
			#print the_page
print "done"

		#sys.exit(1)
#generate_aircraft_minidom(xml_file_path)
		

