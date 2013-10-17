#!/usr/bin/python

# bnguyen - bao@ooyala.com
# set sts=2

class Severity(object):
	# @see http://tumblr.github.com/platform/collinsTutorial/out/logapi.html
	LEVELS = ['EMERGENCY','ALERT','CRITICAL','ERROR','WARNING','NOTICE','INFORMATIONAL','DEBUG','NOTE']

	def __init__(self):
		pass
	# Given a severity level, give back the severity, or None if not valid
	# @param [String,Symbol] level Severity level
	# @return [String] Severity level as string
	def value_of(self, level):
	  level_s = normalize(level)
	  if valid(level_s):
	    return str(level_s)
	  else:
	    return None
	  
	# Convert a level into one appropriate for validating
	# @param [Symbol,String] level Severity level
	# @return [Symbol] normalized (not neccesarily valid) severity level
	def normalize(self, level):
	  #level.to_s.upcase.to_sym
	  return str(level).upper()

	# Check is a level is valid or not
	# @param [Symbol,String] level Severity level
	# @return [Boolean] indicate whether valid or not
	def valid(level):
	  level_s = normalize(level)
	  # return True if i in in self.LEVELS, otherwise return False
	  return [True for i in LEVELS if i == level_s] or False

	#@return [Array<String>] severity levels
	def to_a():
	  return LEVELS