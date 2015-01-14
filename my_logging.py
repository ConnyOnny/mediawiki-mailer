import conf
import logging
import atexit

# use this in the modules like this:
# import my_logging
# logger = my_logging.getLogger(__name__)

logging.basicConfig(filename=conf.logfile)

def getLogger(name):
	logger = logging.getLogger(name)
	logger.setLevel(conf.global_logging_level)
	return logger