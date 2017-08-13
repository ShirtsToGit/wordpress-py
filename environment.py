import os
import sys
"""
 Imports environment specific attributes from local file or CI provided environment variables.
"""

def init(environment_name):
	global user
	global password
	global url
	global store_prefix
	global catalog_dir
	global repo_prefix

	catalog_dir="catalog_dir"
	repo_prefix="https://github.com/ShirtsToGit/catalog/tree/master/shirts/"
	store_prefix="https://teespring.com/"

	if environment_name == "local":
		import test_config
		user=test_config.user
		password=test_config.password
		url=test_config.url
	else:	
		user=os.getenv(environment_name + "_user")
		password=os.getenv(environment_name + "_password")
		url=os.getenv(environment_name + "_url")
