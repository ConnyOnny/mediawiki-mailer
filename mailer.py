import smtplib
import conf
import re
import itertools
import my_logging
import email.utils

logger = my_logging.getLogger(__name__)

_DST_FIELDS = ["to","cc","resent-to","resent-cc"]

def get_mail_destination_addresses (msg):
	dsts = []
	for field in _DST_FIELDS:
		dsts += msg.get_all(field,[])
	adrs_pairs = email.utils.getaddresses(dsts)
	return list(map(lambda x:x[1],adrs_pairs))

def _get_first_group_if_match (strings, regexp):
	matching = []
	for s in strings:
		match = regexp.match(s)
		if match:
			matching.append(match.group(1))
	return matching

def _adr_unescape(adr):
	adr = adr.lower()
	for unic,repl in conf.character_substitutions:
		adr = adr.replace(repl,unic)
	return adr

def get_lists (msg):
	addresses = get_mail_destination_addresses(msg)
	return list(map(_adr_unescape,_get_first_group_if_match(addresses,re.compile(conf.mailing_list_regex))))

def get_users (msg):
	addresses = get_mail_destination_addresses(msg)
	return list(map(_adr_unescape,_get_first_group_if_match(addresses,re.compile(conf.individual_mail_regex))))

def add_listinfo (msg):
	if conf.add_listinfo:
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