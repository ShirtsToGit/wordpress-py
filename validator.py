import requests		


def validate(meta,path,store_prefix,env_name):
	check_slug_validity(meta,path)
	store_url=store_prefix + meta['slug']
	if "store_slug" in meta:
		store_url=store_prefix + meta['store_slug']
	if env_name == "prod":
		check_store_exists(meta,store_url)
	else:
		print "\tWARNGING: Non Prod, not checking for valid store URL"



def check_slug_validity(meta,path):
	if meta['slug']:
		slug = meta['slug']
		if slug != path:
			raise Exception("The defined slug: " + meta['slug'] + " does not equal location " + path)
	else:
		raise Exception("No slug defined")
	
def check_store_exists(meta,store_url):
	slug = meta['slug']
	if "store_slug" in meta:
		slug = meta['store_slug']
	response = requests.get(store_url)
	if response.status_code != 200:
		raise ValidationException("Slug not found in store: " + store_url)


class ValidationException(Exception):
	pass
