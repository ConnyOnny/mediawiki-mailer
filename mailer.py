import smtplib
import conf
import re
import itertools

_extractor_match_ltgt = re.compile("^[^<>]*<([^<>@]+@[^<>@]+)>$")
def extract_mail (s):
	"""
	name <mail@example.com> => mail@example.com
	mail@example.com => mail@example.com
	"""
	match = _extractor_match_ltgt.match(s)
	if match:
		return match.group(1)
	else:
		# change nothing and hope for the best
		return s

def get_lists (msg):
	regexp = re.compile(conf.mailing_list_regex)
	# you could write this whole loop as a single statement with
	# map and filter
	return list(filter(regexp.fullmatch, map(extract_mail, itertools.chain(msg.get_all("To",[]), msg.get_all("Cc",[])))))

def get_article_name (listadr):
	regexp = re.compile(conf.mailing_list_regex)
	match = regexp.fullmatch(listadr)
	if not match:
		raise ValueError('"%s" is not a mailing list address' % listadr)
	return match.group(1)

def add_listinfo (msg):
	msg.add_header("List-Unsubscribe","<mailto:thunis-postmaster@peacock.uberspace.de>")

def send_mail (msg, destinations):
	with smtplib.SMTP(conf.smtp_server, conf.smtp_port) as s:
		s.starttls()
		s.ehlo()
		s.login(conf.smtp_user, conf.smtp_password)
		s.send_message(msg, conf.smtp_srcadr, destinations)