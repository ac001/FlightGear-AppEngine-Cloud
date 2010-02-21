# -*- coding: utf-8 -*-

## Global Config uration for script execution

import os
import sys
import glob
import yaml

#from BeautifulSoup import BeautifulStoneSoup, Tag, NavigableString
#import BeautifulSoup

## TODO make this either env or command line or error
FG_ROOT = '/home/flight-sim/flight-gear-9/data'
FG_DATA_AIRCRAFT_PATH = '%s/Aircraft/' % FG_ROOT

## TODO make this either env or command line or error
YAML_PATH = '/home/flight-sim/fg-aircraft/fg-aircraft.appspot.com/aicraft_yaml'

############################################
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
	
	d={}
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


def generate_aircraft_minidom(xml_file_path):
	try:
		doc = xml.dom.minidom.parse(xml_file_path)
	except :
		print "ERRORsome parse error"
		return

	mapping = {}
	for node in doc.getElementsByTagName("PropertyList"):
		if node.getAttribute("include"):
			print "include", node.getAttribute("include")
		


def generate_aircraft_yaml(xml_contents, file_name):

		## convert string to dictionary
		try:
			xml_dic = xmltodict(xml_contents)
		except:
			print "failed to convert to dict"
			return
		
		if not xml_dic:
			print "ERROR: Something not parsable"
			return
		## include
		#print xml_dic

		## construct yaml dictionary and check for basic values (non conformists ignored for now)
		yaml_dic = {}
		if not 'sim' in xml_dic:
			#print "ERROR: no <sim> tag", file_name
			return
		if not 'aero' in xml_dic['sim'][0]:
			#print "ERROR: no <aero> tag", file_name
			return

		## map xml to yaml
		yaml_dic['aero'] = str(xml_dic['sim'][0]['aero'][0])
		if 'description' in xml_dic['sim'][0]:
			yaml_dic['description'] = str(xml_dic['sim'][0]['description'][0])

		if 'author' in xml_dic['sim'][0]:
			yaml_dic['author'] = str(xml_dic['sim'][0]['author'][0])
		if 'status' in xml_dic['sim'][0]:
			yaml_dic['status'] = str(xml_dic['sim'][0]['status'][0])

		yaml_dic = {}
		flds = [ 'aero', 'description', 'flight-model', 'author', 'status' ]
		for fld in flds:
			if fld in xml_dic['sim'][0]:
				yaml_dic[fld] = str(xml_dic['sim'][0][fld][0])


		## create yaml string
		#yaml_string = yaml.dump(yaml_dic)
		#print "yaml_dic=", yaml_dic
		return yaml_dic
		## write yaml_string to file
		#file_to_write = YAML_PATH + "/" + str(yaml_dic['aero']) + ".yaml"
		# TODO - catch error
		#file_handle = file(file_to_write, 'w')
		#yaml.dump(yaml_dic, file_handle,  default_flow_style=False, explicit_start=True)
		#file_handle.write(yaml_string)
		#file_handle.close()

		#sys.exit(0)


##########################################################################################
## Process and convert aircraft to yaml files
##########################################################################################
print "FG_DATA_AIRCRAFT_PATH =", FG_DATA_AIRCRAFT_PATH

## Get a list of sub directories of aircraft in FG_ROOT/Aircraft/
directories = sorted(os.listdir(FG_DATA_AIRCRAFT_PATH))

# Loop though each subdir
c = 0
print "--------------------------------------------"
for air_dir in directories:

	##  list the *-set.xml files (maybe more than one eg different liveries)
	aircraft_wildpath =  "%s%s/*-set.xml" %(FG_DATA_AIRCRAFT_PATH, air_dir)
	aircraft_set_files = glob.glob(aircraft_wildpath)
	#print aircraft_set_files

	
	#print "###############"
	## Loop thru each xml -set.xml file
	for xml_file_path in aircraft_set_files:
		#print "\nfile=", xml_file_path
		#print xml_file_path

		## read the file contents 
		# TODO - error handler of file read 
		xml_contents =  open(xml_file_path).read()
		#print xml_contents
		#try:
		## parse xml to python dict
		# TODO catch error
		dic = generate_aircraft_yaml(xml_contents, xml_file_path)
		import urllib
		import urllib2
		print "dic=", dic
		if dic == None:
			pass
		else:
			url = 'http://localhost:8080/rpc/aircraft'
			values = {'name' : 'Michael Foord',
					'location' : 'Northampton',
					'language' : 'Python' }
			if 1 == 1:
				data = urllib.urlencode(dic)
				print url + "?" + data
				req = urllib2.Request(url + "?" + data) #, data)
				#req = urllib2.Request(url, data)
				response = urllib2.urlopen(req)
				the_page = response.read()
				print the_page
			c  +=  1
			if c == 20: 
				sys.exit(1)
		#generate_aircraft_minidom(xml_file_path)
		

