#!/usr/bin/env python
import sys
import os
import re

class ApexTopClass:

	def __init__(self, content):
		self.content = content
		self.name = 'UNDEFINED'
		self.inside_class_list = []

		self.find_top_class_name()
		self.get_all_inside_classes()
		

	def find_top_class_name(self):
		pattern = re.compile('(public|global|private).+class ([a-zA-Z0-9_]+)', re.I)

		for line in self.content:
			m = pattern.match(line)
			if (m != None):
				self.name = m[2]
				break 

	def get_all_inside_classes(self):
		pattern = re.compile('(public|global|private).+class ([a-zA-Z0-9_]+)', re.I)

		for line in self.content:
			m = pattern.match(line)
			if m == None : continue
			if m[2] == self.name : continue

			self.inside_class_list.append(m[2])

	def get_references_classes(self, class_list):

		referenced_classes = []
		for line in self.content:
			pattern = re.compile('.*(' + '|'.join(class_list) + ')\.([a-zA-Z0-9_]+)\(.*\)', re.I)
			m = pattern.match(line)
			if m == None : continue
			referenced_classes.append(m[1] + '.' + m[2])

		return list(set(referenced_classes))

	def __str__(self):
		return ('Top level class: ' + self.name)

class Codebase:
	def __init__(self):
		self.class_map = {}

	def add_class(self, cls):
		self.class_map[cls.name] = cls

	def build_edges(self):
		self.edges = {}
		for classname, apexclass in self.class_map.items():
			self.edges[classname] = []
			for referenced_class in apexclass.get_references_classes(self.class_map.keys()):
				self.edges[classname].append(referenced_class)

	def print_edges(self):
		for classname, edge_list in self.edges.items():
			if not edge_list : continue

			print ('### ', classname)

			for edge in edge_list:
				print ('\t\t' + edge)

		print('--------------------------')


def get_filelist(dir):

	pattern = re.compile('.+cls$')

	exclude_pattern = re.compile('(.*test.*)|MetadataService', re.I)

	filelist = [dir + '/' + fn for fn in os.listdir(dir) if (pattern.match(fn) != None and exclude_pattern.match(fn) == None)]
	return filelist

def read_file(fn):
	with open(fn) as f:
		content = f.readlines()
	return [x.strip() for x in content]


def main():
	code_dir = sys.argv[1]
	filelist = get_filelist(code_dir)

	cb = Codebase()

	for fn in filelist:
		apexClass = ApexTopClass(read_file(fn))
		cb.add_class(apexClass)

	cb.build_edges()
	cb.print_edges()



if __name__ == '__main__':
	main()