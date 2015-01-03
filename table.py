import csv

class ThunisDialect(csv.Dialect):
	# comma separated values
	delimiter = ','
	# use escaping: \" instead of ""
	doublequote = False
	escapechar = '\\'
	# unix line endings
	lineterminator = '\n'
	# normal quotes
	quotechar = '"'
	# quote everywhere, this makes the csv more portable
	quoting = csv.QUOTE_ALL
	# strict reading because our file is computer generated
	skipinitialspace = False
	strict = True

csv.register_dialect("thunis", ThunisDialect)

COLUMNS = ["name","email"]

class openWriter:
	def __init__(self,filename):
		self.filename=filename
	def __enter__(self):
		self.f = open(self.filename,"w",newline="")
		self.writer = csv.DictWriter(self.f,fieldnames=COLUMNS,dialect="thunis")
		self.writer.writeheader()
		return self.writer
	def __exit__(self, type, value, tb):
		self.f.close()

class openReader:
	def __init__(self,filename):
		self.filename=filename
	def __enter__(self):
		self.f = open(self.filename,"r",newline="")
		self.reader = csv.DictReader(self.f,dialect="thunis")
		if self.reader.fieldnames != COLUMNS:
			raise Exception('columns in file "%s" were %s but should be %s.' % (self.filename,str(self.reader.fieldnames),str(COLUMNS)))
		return self.reader
	def __exit__(self, type, value, tb):
		self.f.close()

class openAppender:
	def __init__(self,filename):
		self.filename=filename
	def __enter__(self):
		self.f = open(self.filename,"a",newline="")
		self.appender = csv.DictWriter(self.f,fieldnames=COLUMNS,dialect="thunis")
		return self.appender
	def __exit__(self, type, value, tb):
		self.f.close()

class _MailTableIterator:
	def __init__(self,mailTable):
		self.mailTable = mailTable
		self.it = mailTable._name_to_mail.items().__iter__()
	def __next__(self):
		name,email = self.it.__next__()
		return {"name":name,"email":email}

class MailTable:
	def __init__(self,filename):
		self.filename = filename
		self._name_to_mail = {}
		self._mail_to_name = {}
		with openReader(self.filename) as r:
			for row in r:
				self._name_to_mail[row["name"]] = row["email"]
				self._mail_to_name[row["email"]] = row["name"]
	def getMail(self,name):
		return self._name_to_mail[name]
	def getName(self,email):
		return self._mail_to_name[email]
	def __iter__(self):
		return _MailTableIterator(self)