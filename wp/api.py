from pprint import pprint
import simplejson as json
import requests
import imagehash
from PIL import Image
from io import BytesIO

"""
TODO
- Check store for matching URL (should be in MAIN not here...)
- Adding new designs
- Styles (and prices)
- use git hash for design versioing saved as ACF & storeslug
"""


class Wordpress(object):
	def __init__(self,url,usern,passw):
		self.auth = (usern,passw)
		self.url  = url
		self.api_prefix = "/wp-json/wp/v2/"
		print "API initialized to website: " + url

	def publish_design(self,meta,design_path):
		slug = meta['slug']
		r = self.product_by_slug(slug)
		if(r.status_code == 200):
			existing_product = r.json()
			meta['updates'] = 0
			payload={"content":"","acf":{}} #omitting this and WP decides to add "rendered", their API is such a joke
			if len(existing_product) > 0:
				wp_object = existing_product[0]
				print "\tExists, check for updates"
				payload['id']=wp_object['id']
				self.ensure_latest_image(meta,design_path,wp_object,payload)
				self.create_product_payload(meta,existing_product[0],payload)
				if(meta['updates'] > 0):
					print "\tPUTing " + str(meta['updates']) + " changes to website"
					self.update_product(payload)
				else:
					print "\tNo changes to merge, skipping"
				
			else:
				#publish new product.
				print "\tPublishing new design: " + slug
				empty_product={"title":{"raw":""},"product_tag_names":[],"acf":{}}
				self.upload_image(meta,payload,design_path)
				self.create_product_payload(meta,empty_product,payload)
				self.create_product(payload)

	def create_product_payload(self,meta,wp_object,payload):
		if(wp_object['title']['raw'] != meta['title']):
			print "\tChanging title from:\t" + wp_object['title']['raw']
			print "\t\t\tto:\t" + meta['title']
			payload['title'] = meta['title']
			meta['updates']+=1
		if( 'description' not in wp_object['acf']):
			wp_object['acf']['description'] = ""
		if( wp_object['acf']['description'] != '<p>' + self.html_escape(meta['description']) + '</p>\n'):
			print "\tChanging description from: " + repr(wp_object['acf']['description'])
			print "\tto: " + repr(self.html_escape(meta['description']))
			payload['acf']['description'] = meta['description']
			meta['updates']+=1
		if( 'attribution' not in wp_object['acf']):
			wp_object['acf']['attribution'] = ""
		proper_attribution = self.build_attribution_html(meta['attributions'])
		if( wp_object['acf']['attribution'] != proper_attribution + "\n"): # wp or acf plugin adds newline on response string
			print "\tChanging attribution from: " + repr(wp_object['acf']['attribution']) 
			print "\tto: " + repr(proper_attribution)
			payload['acf']['attribution'] = proper_attribution
			meta['updates']+=1
		if( 'charity_name' not in wp_object['acf']):
			wp_object['acf']['charity_name'] = ""
		if( wp_object['acf']['charity_name'] != meta['charity']['name']):
			print "\tChanging charity name from: " + wp_object['acf']['charity_name']
			print "\tto: " + meta['charity']['name']
			payload['acf']['charity_name'] = meta['charity']['name']
			meta['updates']+=1
		if( 'charity_level' not in wp_object['acf']):
			wp_object['acf']['charity_level'] = ""
		if( wp_object['acf']['charity_level'] != str(meta['charity']['percent'])):
			print "\tChanging charity percent from: " + wp_object['acf']['charity_level']
			print "\tto: " + str(meta['charity']['percent'])
			payload['acf']['charity_level'] = str(meta['charity']['percent'])
			meta['updates']+=1
		if( 'charity_link' not in wp_object['acf']):
			wp_object['acf']['charity_link'] = ""
		if( wp_object['acf']['charity_link'] != meta['charity']['link']):
			print "\tChanging charity link from: " + wp_object['acf']['charity_link']
			print "\tto: " + meta['charity']['link']
			payload['acf']['charity_link'] = meta['charity']['link']
			meta['updates']+=1
		if ("store_slug" in meta) and ("store_slug" not in wp_object or wp_object['acf']['store_slug'] != meta['store_slug']):
			print "\tChanging storeslug to: " + meta['store_slug']
			payload['acf']['store_slug'] = meta['store_slug']
			meta['updates']+=1
		if( set(wp_object['product_tag_names']) != set(meta['tags']) ):
			print "\tChanging tags from: " + str(wp_object['product_tag_names'])
			print "\tto: " + str(meta['tags'])
			payload['product_tag_names'] = meta['tags']
			meta['updates']+=1


	def build_attribution_html(self,attributions):
		html_credits=[]
		for credit in attributions:
			html=credit['type']
			if('name' in credit):	
				if "image_link" in credit:
					html+=' <a href="' + credit['image_link'] + '">' + credit['name'] + '</a>'
				else:
					html+=" " + credit['name']
			if( "author" in credit):
				html+=' by <a href="' + credit['author_link'] + '">' + credit['author'] + '</a>.'
			if("license" in credit):
				if "license_link" in credit:
					html+=' License: <a href="' + credit['license_link'] + '">' + credit['license'] + '</a>'
				else:
					html+=" License: " + credit['license']
			html_credits.append(html)
		return '<p>' + '<br />'.join(html_credits) + '</p>'

	'''
	Upload image if different, and flag payload for updates
	'''


	def image_path(self,design_path,meta):
		image_name = meta['design_print']
		if "sample_image" in meta:
			image_name = meta['sample_image']
		image_path = design_path + "/" + image_name
		return image_path

	def ensure_latest_image(self,meta,design_path,existing_product,updated_payload):
		if "design_image" in existing_product['acf']:
			if self.image_hash_equal(self.image_path(design_path,meta),existing_product['acf']['design_image']['url']):
				# no changes needed
				return
		print "\tDesign image missing or altered."
		self.upload_image(meta,updated_payload,design_path)

	def upload_image(self,meta,updated_payload,design_path):
		headers ={
			'Content-Disposition' :  'attachment;filename=' + meta['slug'] + ".png",
			'Content-Type' : 'image/png'
			}
		full_path = self.url + self.api_prefix + "media/"
		image_path = self.image_path(design_path,meta)
		print "\tUploading " + image_path + " to " + full_path
		with open(image_path,'rb') as f:
			response = requests.post(full_path, auth=self.auth, headers=headers, data=f)
		uploaded_media_id = response.json()['id']
		updated_payload['acf']['design_image'] = uploaded_media_id
		meta['updates']+=1


	def image_hash_equal(self,local_path,remote_path):
		print "\tComparing " + local_path + " with " + remote_path
		local_hash = imagehash.dhash(Image.open(local_path))
		remote_hash = imagehash.dhash(Image.open(BytesIO(requests.get(remote_path).content)))
		return local_hash == remote_hash


	def update_product(self, payload):
		path = "products/" + str(payload['id'])
		r = self.post_json(path,payload)
		print "\tResult: " + str(r.status_code)

	def create_product(self, payload):
		path = "products/" 
		r = self.post_json(path,payload)
		print "\tResult: " + str(r.status_code)

	def products(self,search=""):
		path = "products"
		if(search):
			path =  "products?search=" + search
		return self.get(path)

	def product_by_slug(self,slug):
		path =  "products?slug=" + slug + "&context=edit"
		return self.get(path)


	def get(self,path):
		r = requests.get(self.url + self.api_prefix + path, auth=self.auth)
		#print "Response returned: " + str(r.status_code)
		return r

	def post_json(self,path,data):
		r = requests.post(self.url + self.api_prefix + path, auth=self.auth, json=data)
		#print "Response returned: " + str(r.status_code)
		return r





	def html_escape(self,text):
	    """Produce entities within text."""
	    html_escape_table = {
			"&": "&amp;",
			'"': "&quot;",
			"'": "&#8217;",
			">": "&gt;",
			"<": "&lt;",
			}
	    return "".join(html_escape_table.get(c,c) for c in text)
