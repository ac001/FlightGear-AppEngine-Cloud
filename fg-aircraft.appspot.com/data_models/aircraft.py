# -*- coding: utf-8 -*-

class Manufacturers():

	## this class is functions that query and cache.. Aircraft, eg jet egnine, size, seats, etc

	def index(self):
		# psuedo sql = 'select distinct Aircraft.Manufacturer as Manufaturer from Aircraft order by Manufacturer ASC'

	def a2z(self):
		# psuedo sql = 'select distinct(upper((left(Aircraft.Manufacturer)) as a2z from Aircraft order by a2z ASC'




class Aircraft(db.Model):
	#authors = <one to many>
