import urllib.request
import re

import conf

class DownloadFailedException(Exception):
	pass

def get_utf8(url):
	response = urllib.request.urlopen(url)
	return response.read().decode("utf-8")

_user_scanner_re = re.compile('<a href="/wiki/index.php\?title=Benutzer:([^"]+?)"')
def get_users(article):
	try:
		html = get_utf8(conf.article_lookup_url % article)
	except DownloadFailedException:
		return set()
	users = set()
	for match in _user_scanner_re.finditer(html):
		user = match.group(1)
		users.add(user)
	return users