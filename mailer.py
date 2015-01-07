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
	return list(filter(regexp.match, map(extract_mail, itertools.chain(msg.get_all("To",[]), msg.get_all("Cc",[])))))

def get_article_name (listadr):
	regexp = re.compile(conf.mailing_list_regex)
	match = regexp.match(listadr)
	if not match:
		raise ValueError('"%s" is not a mailing list address' % listadr)
	return match.group(1)

def add_listinfo (msg):
	msg.add_header("List-Unsubscribe","<mailto:thunis-postmaster@peacock.uberspace.de>")

def send_mails (l):
	with smtplib.SMTP(conf.smtp_server, conf.smtp_port) as s:
		s.starttls()
		s.ehlo()
		s.login(conf.smtp_user, conf.smtp_password)
		for msg, destinations in l:
			s.send_message(msg, conf.smtp_srcadr, destinations)

def send_mail (msg, destinations):
	send_mails([msg, destinations])