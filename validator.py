import requests			
import wpconfig


def validate(meta,path):
	check_slug_validity(meta,path)
	check_store_exists(meta)



def check_slug_validity(meta,path):
	if meta['slug']:
		slug = meta['slug']
		if slug != path:
			raise Exception("The defined slug: " + meta['slug'] + " does not equal location " + path)
	else:
		raise Exception("No slug defined")
	
def check_store_exists(meta):
	slug = meta['slug']
	if "store_slug" in meta:
		slug = meta['store_slug']
	store_url = wpconfig.store_prefix + slug
	response = requests.get(store_url)
	if response.status_code != 200:
		raise ValidationException("Slug not found in store: " + store_url)


class ValidationException(Exception):
	pass
