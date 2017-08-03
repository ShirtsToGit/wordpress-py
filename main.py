#! /usr/bin/env python
import os
import simplejson as json
from wp.api import Wordpress
import wpconfig

api = Wordpress(wpconfig.url, wpconfig.user, wpconfig.password)
catalog = wpconfig.catalog_dir


#
#  IMportant!   
#  Wordpress team can't figure out API Authentication, ignore their mess and use "Application Passwords" by GeorgeStephanis
#  https://github.com/georgestephanis/application-passwords
#  Depensing on host, (if using CGI) youll need to add https://github.com/georgestephanis/application-passwords/wiki/Basic-Authorization-Header----Missing
#
#



for root, dirs, filenames in os.walk(catalog):
	for dirn in dirs:
		print "Found design folder: " + dirn

	for entry in filenames:
		filename = root + "/" + entry
		if(entry == "meta.json"):
			file = open(filename,'r')
			data = file.read()
			meta = json.loads(data);
			if(meta['slug']):
				print "Operating on " + filename
				api.publish_design(meta)
			else:
				print "No slug defined in meta.json for " + filename


	
