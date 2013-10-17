#!/usr/bin/python

# bnguyen - bao@ooyala.com
# set sts=2

from severity import Severity
from util import parameters as params
import logging

logger = logging.getLogger("collins client")

# Log a message against an asset using the specified level
# @param [String,Collins::Asset] asset
# @param [String] message
# @param [Severity] level severity level to use
# @return [Boolean] true if logged successfully
# @raise [Collins::ExpectationFailed] the specified level was invalid
# @raise [Collins::RequestError,Collins::UnexpectedResponseError] if the asset or message invalid
def log(asset, message, level=None):
  parameters = {
    'message' : message,
    'type' : log_level_from_string(level)
  }
  parameters = params.select_non_empty_parameters(parameters)
  #logger.debug("Logging to #{asset.tag} with parameters #{parameters.inspect}")
  r = http_put("/api/asset/#{asset.tag}/log", parameters, asset.location)
  print r.text
  #  parse_response response, :as : :status, :expects : 201
  
# Fetch logs for an asset according to the options specified
# @example
#   'filter' : "EMERGENCY;ALERT" # Only retrieve emergency and alert messages
#   'filter' : "!DEBUG;!NOTE"    # Only retrieve non-debug/non-notes
# @param [String,Collins::Asset] asset
# @param [Hash] options 'query' options
# @option options [Fixnum] :page (0) Page of results
# @option options [Fixnum] :size (25) Number of results to retrieve
# @option options [String] :sort (DESC) Sort ordering for results
# @option options [String] 'filter' Semicolon separated list of severity levels to include or exclude
# @option options [String] :all_tag If specified, an asset tag is this value, proxy to the all_logs method
# @note To exclude a level via a 'filter' it must be preped with a `!`
# @return [Array<OpenStruct>] Array of log objects
# @raise [Collins::UnexpectedResponseError] on a non-200 response
def logs(asset, options=None):
  all_tag = options.delete(all_tag)
  if all_tag and str(all_tag).lower() == str(asset.tag).lower():
    return all_logs(options)
  
  #parameters = get_page_options(options).merge('filter : get_option('filter', options, None))
  parameters = params.select_non_empty_parameters(parameters)
  #logger.debug("Fetching logs for #{asset.tag} with parameters #{parameters.inspect}")
  r = http_get("/api/asset/#{asset.tag}/logs", parameters, asset.location)
  print r.text
  #  parse_response response, :as : :paginated, :default : [], :raise : strict?, :expects : 200 do |json|
  #    json.map{|j| OpenStruct.new(symbolize_hash(j))}
    
# new solr interface
def search_logs(options=None):
  parameters = get_page_options(options)

  parameters = dict(parameters.items() + {
    'query' : get_option('query', options, None),
    'sortField' : get_option('sortField', options, 'ID')
  }.items())

  parameters = params.select_non_empty_parameters(parameters)
  #logger.debug("Fetching logs for all assets with parameters #{parameters.inspect}")
  r = http_get("/api/assets/logs/search", parameters)
  print r.text
  #  parse_response response, :as : :paginated, :default : [], :raise : strict?, :expects : 200 do |json|
  #    json.map{|j| OpenStruct.new(symbolize_hash(j))}
    
# Same as logs but for all assets
# @see #logs
def all_logs(options=None):
  parameters = get_page_options(options)
  parameters = dict(paramters.items() + {'filter' : get_option('filter', options, None)}.items())
  parameters = params.select_non_empty_parameters(parameters)
  #logger.debug("Fetching logs for all assets with parameters #{parameters.inspect}")
  r = http_get("/api/assets/logs", parameters)
  print r.text
    # parse_response response, :as : :paginated, :default : [], :raise : strict?, :expects : 200 do |json|
    #   json.map{|j| OpenStruct.new(symbolize_hash(j))}
    
def log_level_from_string(level):
  if level and level is None:
    return None
  s = Severity()
  if s.valid(level):
    return s.value_of(level)
  else:
    #raise Collins::ExpectationFailedError.new("#{level} is not a valid log level")
    print "not valid level %s" % level


if __name__ == "__main__":
  pass