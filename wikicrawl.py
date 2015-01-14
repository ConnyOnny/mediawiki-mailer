import urllib.parse
import urllib.error
import urllib.request
import re

import conf

class DownloadFailedException(Exception):
	pass

def get_utf8(url):
	try:
		response = urllib.request.urlopen(url)
		return response.read().decode("utf-8")
	except urllib.error.HTTPError as e:
		raise DownloadFailedException() from e

def get_article_source(article):
	article = urllib.parse.quote(article)
	return get_utf8(conf.article_lookup_url % article)

_user_scanner_re = re.compile('<a href="/wiki/index.php\?title=Benutzer:([^"&]+?)[&"]')
def get_users(article):
	article = article.lower()
	for unic,repl in conf.character_substitutions:
		article = article.replace(repl,unic)
	print(article)
	try:
		html = get_article_source(article)
	except DownloadFailedException as e:
		print(e)
		return set()
	users = set()
	for match in _user_scanner_re.finditer(html):
		user = match.group(1).replace('_',' ')
		users.add(user)
	return users