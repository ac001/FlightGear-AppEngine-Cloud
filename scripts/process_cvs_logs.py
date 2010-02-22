#!/usr/bin/env python
# -*- coding: utf-8 -*-

import conf
import os
import sys

class ProcessLogs:

	def __init__(self):
		self.reset()

		self.records = []

	def reset(self):
		self.rcs = {}
		self.in_rcs = False
		self.in_revision = False
		self.rev = {}
		self.comment_lines = None

	def run(self):
		files = sorted(os.listdir(conf.ROOT_PATH + "/temp/logs/"))
		for file_name in files:
			self.file_name = file_name
			self.records = []
			self.reset()
			contents = open(conf.ROOT_PATH + "/temp/logs/" + file_name, "r").read()
			lines = contents.split("\n")
			print "----------------------------___"
			for line in lines:
				#print "line=", line
				line = line.strip()

				self.process_line(line)
			print self.records
			sys.exit(0)

	def process_line(self, line):
		#print line
		if line == "----------------------------":
			self.in_revision = 1
			self.rev = {}
			return

		if self.in_revision == 1 and line.startswith("revision"):
			self.rev['revision'] = line.split(" ", 1)[1]
			return
	
		if self.in_revision == 1 and line.startswith("date"):
			sections = line.split(";")
			for sec in sections:
				if sec.find(":") > 1:
					parts = sec.split(":", 1)
					self.rev[parts[0].strip()] = parts[1].strip()

			self.in_revision = "comment"
			self.comment_lines = []
			return

		if line.startswith("========================"):
			#print "END"
			self.rev['message'] = "\n".join(self.comment_lines)
			#print "MESS", self.comment_lines , "\n".join(self.comment_lines)
			#print "rcs=", self.rcs
			#print "rev=", self.rev
			self.records.append([self.rcs.copy(), self.rev.copy()])
			self.reset()
			return

	
		if self.in_revision == "comment":
			self.comment_lines.append(line)
			return

		sections = line.split(";")
		if len(sections) == 1:
			parts = sections[0].split(":")
			if parts[0] == 'RCS file':
				in_rcs = True
				self.rcs = {}
				self.rcs['file'] = parts[1].replace("/var/cvs/FlightGear-0.9/data/Aircraft/" + self.file_name[:-4] + "/", "")[:-2]
				self.rcs['rcs'] = parts[1]
				return

			if parts[0] == 'head':
				self.rcs['head'] = parts[1]
				return



p = ProcessLogs()
p.run()
print "--"