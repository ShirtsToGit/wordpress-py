			
def check_slug_validity(meta,path):
	if meta['slug']:
		slug = meta['slug']
		if slug != path:
			raise Exception("The defined slug: " + meta['slug'] + " does not equal location " + path)
	else:
		raise Exception("No slug defined")
	
