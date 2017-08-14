#! /usr/bin/env python
import os
import sys
import simplejson as json
from wp.api import Wordpress
import environment as wpconfig
import validator

if len(sys.argv) != 2:
	print "Usage:\n\t" + sys.argv[0] + " <env_name>"
	exit()
else:
	env_name = sys.argv[1]

wpconfig.init(env_name)
print "URL: " + wpconfig.url 
print "Catlog: " + wpconfig.catalog_dir 
api = Wordpress(wpconfig)
catalog = wpconfig.catalog_dir


#
#  IMportant!   
#  Wordpress team can't figure out API Authentication, ignore their mess and use "Application Passwords" by GeorgeStephanis
#  https://github.com/georgestephanis/application-passwords
#  Depensing on host, (if using CGI) youll need to add https://github.com/georgestephanis/application-passwords/wiki/Basic-Authorization-Header----Missing
#
#
designs=0
for root, dirs, filenames  in os.walk(catalog):
	print "Inspecting catalog path: " + root
	for dir__ in dirs:
		print "Inspecting design: " + dir__
		for design, subfolders, assets in os.walk(root + "/" + dir__):
			for asset in assets:
				if(asset == "meta.json"):
					# print "dir__" + dir__
					# print "Design:" + design
					# print "asset:" + asset
					filename = design + "/" + asset
					file = open(filename,'r')
					data = file.read()
					meta = json.loads(data);
					try:
						validator.validate(meta,dir__,wpconfig.store_prefix,env_name)
						api.publish_design(meta,design)
						designs+=1
					except validator.ValidationException as e:
						print "\t" + str(e)
					
	break #dont repeat this loop for subfolders, we handled aboce.

if designs < 1:
	print "ERROR: No designs published/present"
	exit(2)