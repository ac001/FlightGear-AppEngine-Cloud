# -*- coding: utf-8 -*-

import os
import sys


GAE = "fg-aircraft"
## Root path of the google application project
ROOT_PATH = "/home/flight-sim/fg-aircraft/"

## DLight Gear Root
FG_ROOT = '/home/flight-sim/flight-gear-9/data'
FG_DATA_AIRCRAFT_PATH = '%s/Aircraft/' % FG_ROOT


## place to spool bits and dics as cvs import
CVS_LOGS = '/home/flight-sim/fg-aircraft/temp/logs/'
CVS_DIC = '/home/flight-sim/fg-aircraft/temp/dic/'

#YAML_PATH = '/home/flight-sim/fg-aircraft/fg-aircraft.appspot.com/aicraft_yaml'

## path to the fgmap repos
FG_MAP_ROOT = '/home/flight-sim/public_html/fgmap'

if "--live" in sys.argv:
	WWW = "http://%s.appspot.com" % GAE
else:
	WWW = "http://localhost:8080"