# -*- coding: utf-8 -*-

## Global Config uration for script execution

import os
import sys
import glob
import yaml

import urllib
import urllib2


## TODO make this either env or command line or error
FG_ROOT = '/home/flight-sim/flight-gear-9/data'
FG_DATA_AIRCRAFT_PATH = '%s/Aircraft/' % FG_ROOT

FGMAP_ROOT ='/home/flight-sim/public_html/fgmap'


##########################################################################################
print "FGMAP_ROOT =", FGMAP_ROOT

## Get a list of sub directories of aircraft in FG_ROOT/Aircraft/

content = open(FGMAP_ROOT + "/fgmap.servers").read()
lines = content.split("\n")
print lines

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
		print "mp=", line
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
		url = "http://localhost:8080/mpservers/import/"
		if 1 == 1:
			data = urllib.urlencode(dic)
			print url + "?" + data
			req = urllib2.Request(url + "?" + data) #, data)
			#req = urllib2.Request(url, data)
			response = urllib2.urlopen(req)
			the_page = response.read()
			print the_page


		#sys.exit(1)
#generate_aircraft_minidom(xml_file_path)
		

