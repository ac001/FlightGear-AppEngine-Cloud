# -*- coding: utf-8 -*-

## Global Config uration for script execution

import os
import glob

FG_DATA_AIRCRAFT = '/home/flight-sim/flight-gear-9/data/Aircraft/'

#APP_ROOT = os.path.join(__file__)
#print APP_ROOT

print "FG_DATA_AIRCRAFT =", FG_DATA_AIRCRAFT
directories = sorted(os.listdir(FG_DATA_AIRCRAFT))

#print "\n".join(directories)
for air_dir in directories:
	aircraft_wildpath =  "%s%s/*-set.xml" %(FG_DATA_AIRCRAFT, air_dir)
	#print aircraft_wildpath
	print "--------------------------------\n"
	aircraft_sets = glob.glob(aircraft_wildpath)
	print aircraft_sets

	for xml_file in aircraft_sets:
		print xml_file
		