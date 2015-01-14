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

def _get_by_regex (msg, regexp):
	matching = []
	for adr in itertools.chain(msg.get_all("To",[]), msg.get_all("Cc",[])):
		adr = extract_mail(adr)
		match = regexp.match(adr)
		if match:
			matching.append(match.group(1))
	return matching

def _adr_unescape(adr):
	adr = adr.lower()
	for unic,repl in conf.character_substitutions:
		adr = adr.replace(repl,unic)
	return adr

def get_lists (msg):
	return _adr_unescape(_get_by_regex(msg,re.compile(conf.mailing_list_regex)))

def get_users (msg):
	return _adr_unescape(_get_by_regex(msg,re.compile(conf.individual_mail_regex)))

def add_listinfo (msg):
	msg.add_header("List-Unsubscribe",conf.unsubscribe_header)

def send_mails (l):
	with smtplib.SMTP(conf.smtp_server, conf.smtp_port) as s:
		s.starttls()
		s.ehlo()
		s.login(conf.smtp_user, conf.smtp_password)
		for msg, destinations in l:
			s.send_message(msg, conf.smtp_srcadr, destinations)

def send_mail (msg, destinations):
	send_mails([(msg, destinations)])