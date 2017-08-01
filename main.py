import os
from wp.api import Wordpress
import wpconfig

wp = Wordpress("https://test.shirtstogit.com",wpconfig.key,wpconfig.secret)

posts = wp.posts()
print posts
