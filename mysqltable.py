import cymysql
import my_logging

import conf

logger = my_logging.getLogger(__name__)

class MailTable:
	def __init__(self):
		self._conn = cymysql.connect(host=conf.mysql_server, user=conf.mysql_user, passwd=conf.mysql_password, db=conf.mysql_database, charset='utf8')
	def get_mail(self,name):
		cur = self._conn.cursor()
		cur.execute("select user_email from user where user_name = %s", (name,))
		rows = cur.fetchall()
		assert len(rows) == 0 or len(rows) == 1
		if len(rows) == 0:
			return None
		else:
			return rows[0][0].decode('utf-8')
	def get_name(self,email):
		raise NotImplemented()
	def __iter__(self):
		raise NotImplemented()