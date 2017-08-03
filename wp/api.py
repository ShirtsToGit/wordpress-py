from pprint import pprint
import simplejson as json
import requests

"""
TODO
- Models
- 
"""


class Wordpress(object):
	def __init__(self,url,usern,passw):
		self.auth = (usern,passw)
		self.url  = url
		self.api_prefix = "/wp-json/wp/v2/"
		print "API initialized to website: " + url

	def publish_design(self,meta):
		slug = meta['slug']
		r = self.product_by_slug(slug)
		if(r.status_code == 200):
			existing_product = r.json()
			if len(existing_product) > 0:
				print "\tExists, check for updates"
				design_patch = self.create_patch(meta,existing_product[0])
				if(meta['updates'] > 0):
					print "\tPUTing " + str(meta['updates']) + " changes to website"
					self.update_product(design_patch)
				else:
					print "\tNo changes to merge, skipping"
				
			else:
				#publish new product.
				print "\tPublishing new design: " + slug

	def create_patch(self,meta,wp_object):
		updates = 0
		payload={}
		payload['id']=wp_object['id']
		payload['acf']={}

		if(wp_object['title']['rendered'] != meta['title']):
			print "\tChanging title from:\t" + wp_object['title']['rendered']
			print "\t\t\tto:\t" + meta['title']
			payload['title'] = meta['title']
			updates = updates + 1
		if( 'description' not in wp_object['acf']):
			wp_object['acf']['description'] = ""
		if( wp_object['acf']['description'] != meta['description']):
			print "\tChanging description from: " + wp_object['acf']['description']
			print "\tto: " + meta['description']
			payload['acf']['description'] = meta['description']
			updates = updates + 1
		if( 'charity_name' not in wp_object['acf']):
			wp_object['acf']['charity_name'] = ""
		if( wp_object['acf']['charity_name'] != meta['charity']['name']):
			print "\tChanging name from: " + wp_object['acf']['charity_name']
			print "\tto: " + meta['charity']['name']
			payload['acf']['charity_name'] = meta['charity']['name']
			updates = updates + 1
		if( 'charity_level' not in wp_object['acf']):
			wp_object['acf']['charity_level'] = ""
		if( wp_object['acf']['charity_level'] != str(meta['charity']['percent'])):
			print "\tChanging percent from: " + wp_object['acf']['charity_level']
			print "\tto: " + str(meta['charity']['percent'])
			payload['acf']['charity_level'] = str(meta['charity']['percent'])
			updates = updates + 1
		if( 'charity_link' not in wp_object['acf']):
			wp_object['acf']['charity_link'] = ""
		if( wp_object['acf']['charity_link'] != meta['charity']['link']):
			print "\tChanging link from: " + wp_object['acf']['charity_link']
			print "\tto: " + meta['charity']['link']
			payload['acf']['charity_link'] = meta['charity']['link']
			updates = updates + 1
		meta['updates'] = updates
		return payload

	def update_product(self, payload):
		path = "products/" + str(payload['id'])
		r = self.post(path,payload)
		print "\tResult: " + str(r.status_code)

	def products(self,search=""):
		path = "products"
		if(search):
			path =  "products?search=" + search
		return self.get(path)

	def product_by_slug(self,slug):
		path =  "products?slug=" + slug
		return self.get(path)


	def get(self,path):
		r = requests.get(self.url + self.api_prefix + path, auth=self.auth)
		#print "Response returned: " + str(r.status_code)
		return r

	def post(self,path,data):
		r = requests.post(self.url + self.api_prefix + path, auth=self.auth, json=data)
		#print "Response returned: " + str(r.status_code)
		return r
