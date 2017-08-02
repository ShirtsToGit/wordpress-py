#! /usr/bin/env python
import os
import simplejson as json
from wp.api import Wordpress
import wpconfig

api = Wordpress("https://test.shirtstogit.com",wpconfig.key,wpconfig.secret)
catalog = "shirts"
cwd = os.getcwd()

# r = wp.products()
# print "All Product\n" + r.text
# r = wp.products("resist")
# print "Search Product\n" + r.text
for root, dirs, filenames in os.walk(catalog):
	for entry in filenames:
		filename = root + "/" + entry
		print "Inspecting " + filename
		if(entry == "meta.json"):
			file = open(filename,'r')
			data = file.read()
			meta = json.loads(data);
			if(meta['slug']):
				api.publish_design(meta)
			else:
				print "No slug defined in meta.json"

	
