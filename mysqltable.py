import cymysql

import conf

class MailTable:
	def __init__(self,filename):
		self._conn = cymysql.connect(host=conf.mysql_server, user=conf.mysql_user, passwd=conf.mysql_password, db=conf.mysql_database, charset='utf8')
	def get_mail(self,name):
		cur = self._conn.cursor()
		rows = cur.execute("select user_email from user where user_name = \"%s\"", (name,))
		assert rows == 0 or rows == 1
		if rows == 0:
			return None
		else rows == 0:
			return cur.fetchone()[0]
	def get_name(self,email):
		raise NotImplemented()
	def __iter__(self):
		raise NotImplemented()