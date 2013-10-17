#!/usr/bin/python

# bnguyen - bao@ooyala.com
# set sts=2

# useful logging info
# http://www.red-dove.com/python_logging.html
# http://www.shutupandship.com/2012/02/how-python-logging-module-works.html


import logging
import sys

DEFAULT_LOG_FORMAT = "%Y-%m-%d %H:%M:%S.%L"

def get_logger(options=None):

  #TODO: impletement options
  #if options['logger']:
  #  return options['logger']
  # trace = Collins::Option(options[:trace]).get_or_else(false)
  # debug = Collins::Option(options[:debug]).get_or_else(false)
  # progname = Collins::Option(options[:progname] || options[:program]).get_or_else('unknown')
  # logfile = Collins::Option(options[:logfile]).get_or_else(STDOUT)

  # TODO: implement Options
  trace = False
  debug = True
  programme = "collins client"
  logfile = "STDOUT"

  # create logger
  logger = logging.getLogger(programme)
  
  if trace:
    logger.setLevel(logging.TRACE)
  elif debug:
    logger.setLevel(logging.DEBUG)
  else:
    logger.setLevel(logging.INFO)

  # add a file handler
  #fh = logging.FileHandler('myapp.log')
  #fh.setLevel(logging.WARNING)

  # add the stdout handler
  fh = logging.StreamHandler(sys.stdout)
  fh.setLevel(logging.DEBUG)

  # create a formatter and set the formatter for the handler.
  frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  fh.setFormatter(frmt)
  # add the Handler to the logger
  logger.addHandler(fh)

  return logger

if __name__ == "__main__":
  logger = get_logger()
  # You can now start issuing logging statements in your code
  logger.debug('debug message') # This won't print to myapp.log
  logger.info('info message') # Neither will this.
  logger.warn('Checkout this warning.') # This will show up in the log file.
  logger.error('An error goes here.') # and so will this.
  logger.critical('Something critical happened.') # and this one too.
