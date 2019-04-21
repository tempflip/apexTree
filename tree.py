#!/usr/bin/env python
import sys
import os
import re

class ApexTopClass:

	def __init__(self, content):
		self.content = content
		self.name = 'UNDEFINED'

		self.find_top_class_name()

	def find_top_class_name(self):
		pattern = re.compile('(public|global|private).+class ([a-zA-Z0-9_]+)', re.I)

		for line in self.content:
			m = pattern.match(line)
			if (m != None):
				self.name = m[2]
				break 


	def __str__(self):
		return ('Top level class: ' + self.name)

def get_filelist(dir):

	pattern = re.compile('.+cls$')

	filelist = [dir + '/' + fn for fn in os.listdir(dir) if pattern.match(fn) != None]
	return filelist

def read_file(fn):
	with open(fn) as f:
		content = f.readlines()
	return [x.strip() for x in content]


def main():
	code_dir = sys.argv[1]
	filelist = get_filelist(code_dir)

	class_list = []

	for fn in filelist:
		apexClass = ApexTopClass(read_file(fn))
		class_list.append(apexClass)
	
		print (apexClass)		



if __name__ == '__main__':
	main()