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

#########################################
## XML to Dict parser.
## Thanks to http://nonplatonic.com/ben.php?title=python_xml_to_dict_bow_to_my_recursive_g&more=1&c=1&tb=1&pb=1
## for this xml parser
import xml.dom.minidom

def xmltodict(xmlstring):
	doc = xml.dom.minidom.parseString(xmlstring)
	remove_whilespace_nodes(doc.documentElement)
	return elementtodict(doc.documentElement)

def elementtodict(parent):
	child = parent.firstChild
	if (not child):
		return None
	elif (child.nodeType == xml.dom.minidom.Node.TEXT_NODE):
		return child.nodeValue
	
	d = {}
	while child is not None:
		if (child.nodeType == xml.dom.minidom.Node.ELEMENT_NODE):
			try:
				d[child.tagName]
			except KeyError:
				d[child.tagName]=[]
			d[child.tagName].append(elementtodict(child))
		child = child.nextSibling
	return d

def remove_whilespace_nodes(node, unlink=True):
	remove_list = []
	for child in node.childNodes:
		if child.nodeType == xml.dom.Node.TEXT_NODE and not child.data.strip():
			remove_list.append(child)
		elif child.hasChildNodes():
			remove_whilespace_nodes(child, unlink)
	for node in remove_list:
		node.parentNode.removeChild(node)
		if unlink:
			node.unlink()


###################################################################
## Process CVS Aaircraft
###################################################################
class ProcessCVSAircraft:

	def __init__(self):
		self.doc = None
		self.curr_dir = None
		self.errors  = []


	def run(self):
		directories = sorted(os.listdir(conf.FG_DATA_AIRCRAFT_PATH))
		c = 0
		print "\n\nSTART --------------------------------------------"
		for air_dir in directories:
			
			##  list the *-set.xml files (maybe more than one eg different liveries)
			self.curr_dir = air_dir
			aircraft_wildpath =  "%s%s/*-set.xml" %(conf.FG_DATA_AIRCRAFT_PATH, self.curr_dir)
			aircraft_set_files = glob.glob(aircraft_wildpath)
			self.errors = []
			for xml_file_path in aircraft_set_files:
				#print "--------------------------------\n"
				print "set=", self.curr_dir
				
				doc = self.process_set(xml_file_path)
				#if 'version' in self.dic:
				#	print "YYYYYYESSSSSSSS", self.dic
					#sys.exit(0)
				#files_pth = conf.ROOT_PATH + "/temp/json/" + self.curr_dir + '.txt'
				#print files_pth
				#contents = open(files_pth, "r").read()
				
				#self.dic['files'] = contents

				#self.send_to_server( self.dic )

				#print "======================================================"
				c  +=  1
				if 1 == 1 and c == 5: 
					sys.exit(1)
		print self.errors


	def process_set(self, xml_file_path):
		self.dic = {}
		self.dic['directory'] = self.curr_dir
		self.xml_doc(xml_file_path)
		
	def xml_doc(self, xml_file_path):
		#try:
		self.doc = xml.dom.minidom.parse(xml_file_path)
		#except :
		#	print "ERRORsome parse error", xml_file_path
		#	self.errors.append({'parse1': xml_file_path})
		#	return

		mapping = {}
		for node in self.doc.getElementsByTagName("PropertyList"):
			if node.getAttribute("include"):
				#print "include", node.getAttribute("include"), self.curr_dir, xml_file_path
				inc_path = conf.FG_DATA_AIRCRAFT_PATH +  self.curr_dir + "/" +  node.getAttribute("include")
				#print "include=", inc_path
				self.xml_doc(inc_path)

			xml_contents =  open(xml_file_path).read()
			#print xml_cotents
			pro = self.process_file(xml_contents, xml_file_path)
			if pro == None:
				pass #print "ERROR on file"
			else:
				self.dic.update( pro ) 

	
	def process_file(self, xml_contents, file_name):

		#try:
		xml_dic = xmltodict(xml_contents)
		#except:
			#print "failed to convert to dict", file_name
			#self.errors.append({'fail': file_name})
			#return
		
		if not xml_dic:
			print "ERROR: Something not parsable", file_name
			self.errors.append({'parse2': file_name})
			return


		yaml_dic = {}
		if 'sim' in xml_dic:
			flds = [ 'aero', 'description', 'flight-model', 'author', 'status', 'version']
			for fld in flds:
				if fld in xml_dic['sim'][0]:
					yaml_dic[fld] = str(xml_dic['sim'][0][fld][0]).strip().replace("\n","")

			if 'startup' in xml_dic['sim'][0]:
				if 'splash-texture' in xml_dic['sim'][0]['startup'][0]:
					yaml_dic['splash'] = str(xml_dic['sim'][0]['startup'][0]['splash-texture'][0])

			#if 'startup' in xml_dic['sim'][0]:
			if 'engines' in xml_dic:
				#print "**********************************************"
				yaml_dic['engines'] = len(xml_dic['engines'][0]['engine'])
				#print yaml_dic['engines']
				#print "************"

		return yaml_dic



	def send_to_server(self, dic):
		url = conf.WWW + '/import/aircraft/'
		#sprint "URL=", url
		data = urllib.urlencode(dic)
		#print url + "?" + data
		req = urllib2.Request(url, data) #+ "?" + data) #, data)
		#req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		the_page = response.read()
		print the_page

			

p = ProcessCVSAircraft()
p.run()

