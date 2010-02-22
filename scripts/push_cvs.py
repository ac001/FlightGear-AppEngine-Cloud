#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Global Config uration for script execution

import os
import sys
#import glob
#import yaml
import json

import urllib
import urllib2

import conf


###################################################################
## Process CVS Aaircraft
###################################################################
class PushAircraftRevisions:

	def __init__(self):
		self.doc = None
		self.curr_dir = None

	def run(self):
		pth =conf.ROOT_PATH + "temp/json/"
		print pth
		files = sorted(os.listdir(pth))
		c = 0
		print "\n\nSTART --------------------------------------------"
		for f in files:
		
			file_pth = conf.ROOT_PATH + "/temp/json/" + f
			print "file=", file_pth
			contents = open(file_pth, "r").read()
			
			#print json.loads(contents)
			dic = {'revisions': contents}
			self.send_to_server( dic )
			#sys.exit(1)
			#print "======================================================"
			c  +=  1
			if c == 5: 
				print "kill"
				#sys.exit(1)


	def send_to_server(self, dic):
		#json_str = json.dumps(dic)
		url = 'http://localhost:8080/import/revisions/'
		#print json_str

		data = urllib.urlencode(dic)
		#print url + "?" + data
		req = urllib2.Request(url, data) #+ "?" + data) #, data)
		#req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		the_page = response.read()
		print the_page

			

p = PushAircraftRevisions()
p.run()

