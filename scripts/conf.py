# -*- coding: utf-8 -*-

import os




ROOT_PATH = "/home/flight-sim/fg-aircraft/"

FG_ROOT = '/home/flight-sim/flight-gear-9/data'
FG_DATA_AIRCRAFT_PATH = '%s/Aircraft/' % FG_ROOT

CVS_LOGS = '/home/flight-sim/fg-aircraft/temp/logs/'
CVS_DIC = '/home/flight-sim/fg-aircraft/temp/dic/'

YAML_PATH = '/home/flight-sim/fg-aircraft/fg-aircraft.appspot.com/aicraft_yaml'


def aircraft_directories(self):
	return sorted(os.listdir(FG_DATA_AIRCRAFT_PATH))
	
