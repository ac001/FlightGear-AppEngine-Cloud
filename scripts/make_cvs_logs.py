#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess #import call

import conf

directories = sorted(os.listdir(conf.FG_DATA_AIRCRAFT_PATH))
# Loop though each subdir
c = 0
print "--------------------------------------------"
for air_dir in directories:
	cvs_path = conf.FG_DATA_AIRCRAFT_PATH  + air_dir
	is_dir = os.path.isdir(cvs_path)
	if is_dir:
		print "\n----- " + air_dir
		bufsize = 6000
		command = "cvs log -N -r ./%s" % air_dir
		p = subprocess.Popen([command], shell=True, bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		(child_stdin, child_stdout) = (p.stdin, p.stdout)

		text = child_stdout.read()
	
		txtfile = conf.ROOT_PATH + 'temp/logs/' + air_dir + '.txt'
		print txtfile
		f = open(txtfile, 'w')
		f.write(text)
		f.close()
		
		#command = "ls %s" % cvs_path
		#print "command=", command
		#foo =""
		#os.system("ls")
		#print foo
		#res = subprocess.Popen([command])
		#print res
		#sys.exit(0)