from wordpress import API

"""
TODO
- Models
- 
"""


class Wordpress(object):
	def __init__(self, url, key, secret):
		self.wpapi = API(
		    url=url,
		    consumer_key=key,
		    consumer_secret=secret,
		    api="wp-json",
		    version="wp/v2"
		)

	def publish_design(self,meta):
		slug = meta['slug']
		print "Publishing design: " + slug
		r = self.product_by_slug("its-gneiss")
		if(r.status_code == 200):
			#product exists, update
			print "UPdating: " + slug
		else:
			#publish new product.
			print "Publishing new product at " + slug





	def products(self,search=""):
		path = "products"
		if(search):
			path =  "products?search=" + search
		return self.wpapi.get(path)

	def product_by_slug(self,slug):
		path =  "products?slug=" + slug
		return self.wpapi.get(path)
