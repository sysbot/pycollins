#!/usr/bin/python

# bnguyen - bao@ooyala.com
# set sts=2


# local
from asset import Asset
from asset import AssetClient
from api.util import parameters as params
from api import ip_address as ipaddress
from api.util import http_handler
from api.util import parameters as params
import logger


# client = Client.new()
# client.get 'asset_tag'
class Client(object):
  def __init__(self):
    self.logger = logger.get_logger()

  # Create an a Collins asset from a tag name
  # @note n/a
  # @param [String] asset tag name
  # @param [Dict] options
  # @return [Dict] return status in dict
  def create_asset_from_tag(self, asset, **kwargs):
    parameters = {
      "generate_ipmi": params.get_option('generate_ipmi', kwargs, "False"), 
      "status": params.get_option('status', kwargs, "Unallocated"),
      "type": params.get_option('status', kwargs, "SERVER_NODE"), 
    }  
    # TODO: logger - creating asset
    r = http_handler.http_put("/api/asset/%s" % asset, parameters)
    print(r.text)

  # Create an a Collins asset from Asset object
  # @note n/a
  # @param [Asset] asset object
  # @return [Dict] return status in dict
  def create_asset(self, asset, **kwargs):
    parameters = {
      "generate_ipmi": params.get_option('generate_ipmi', kwargs, "False"), 
      "status": params.get_option('status', kwargs, "Unallocated"),
      "type": params.get_option('type', kwargs, "SERVER_NODE"), 
    }    
    # TODO: logger - creating asset
    r = http_handler.http_put("/api/asset/%s" % asset.tag, asset.to_json())
    print(r.text)

  def set_status(self, asset, **kwargs):
    parameters = {
      "status": params.get_option('status', kwargs, "Unallocated"),
      "reason": params.get_option('reason', kwargs, "None")
    }    
    r = http_handler.http_post("/api/asset/%s" % asset.tag, parameters)
    print(r.text)

  def delete_asset(self, asset, **kwargs):
    parameters = {
      "reason": params.get_option('reason', kwargs, "None")
    }
    r = http_handler.http_delete("/api/asset/%s" % asset.tag, parameters)
    print(r.text)

  def get_asset(self, asset, **kwargs):
    parameters = {
      #:location => params.get_option(:location, options, nil)
    }
    #parameters = params.select_non_empty_parameters(parameters)
    #logger.debug("Getting asset %s with params #{parameters.inspect}" % (asset.tag))
    r = http_handler.http_get("/api/asset/%s" % asset.tag, parameters)
    #print(r.text)
    return r.text

  def create_ipmi(self, asset, username, password, address, gateway, netmask):
    self.ipmi_update(asset, {'username': username, 'password': password, 'address': address,
                              'gateway': gateway, 'netmask': netmask})

  def update_ipmi(self, asset):
    parameters = {
      'username': str(asset.ipmi.username),
      'password': str(asset.ipmi.password),
      'address': str(asset.ipmi.address),
      'gateway': str(asset.ipmi.gateway),
      'netmask': str(asset.ipmi.netmask)
    }
    parameters = params.select_non_empty_parameters(parameters)
    if not parameters:
      return True
    #logger.debug("Updating asset %s IPMI info with parameters #{parameters.inspect}" % (asset.tag))
    r = http_handler.http_post("/api/asset/%s/ipmi" % asset.tag, parameters) 
    print (r.text)

  def update_tag_ipmi(self, asset, **kwargs):
    # NOTE: there's a length minimun for the password!! imposed by Collins!!!
    parameters = {
      'username': params.get_option('username', kwargs, None),
      'password': params.get_option('password', kwargs, None),
      'address': params.get_option('address', kwargs, None),
      'gateway': params.get_option('gateway', kwargs, None),
      'netmask': params.get_option('netmask', kwargs, None)
    }
    parameters = params.select_non_empty_parameters(parameters)
    if not parameters:
      return True
    #logger.debug("Updating asset %s IPMI info with parameters #{parameters.inspect}" % (asset.tag))
    r = http_handler.http_post("/api/asset/%s/ipmi" % asset, parameters) 
    print (r.text)
    #for respond in r:
    #  parse_response (response, :expects => [200,201], :as => :status)

  def get_status(self, asset):
    return self.status

  def get_assets(self):
    print (http_handler.http_get('/api/assets').text)

  # @return [String] Collins::Client(host = hostname)
  def __str__():
    "Collins::Client(host = %s)" % self.host

  # @see Collins::Api#strict?
  def strict(default = False):
    self.strict or default

  # Use the specified asset for subsequent method calls
  # @param [Collins::Asset,String] asset The asset to use for operations
  # @return [Collins::AssetClient] Provides most of the same methods as {Collins::Client} but with no need to specfiy the asset for those methods
  def with_asset(asset):
    return AssetClient(asset, self, self.logger)

  #def _fix_hostname(hostname):
  #  hostname.is_a?(String) ? hostname.gsub(/\/+$/, '') : hostname
