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

	def posts(self):
		return self.wpapi.get("posts")