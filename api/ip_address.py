#!/usr/bin/python

# bnguyen - bao@ooyala.com
# set sts=2

from util import parameters as params
from util import http_handler
import logging

logger = logging.getLogger("collins client")

# { "data" : { "ADDRESSES" : [ { "ADDRESS" : "10.25.0.2",
#             "ASSET_ID" : 2,
#             "ASSET_TAG" : "abc",
#             "GATEWAY" : "10.25.0.1",
#             "ID" : 1,
#             "NETMASK" : "255.255.254.0",
#             "POOL" : "SJ-MGMT-IPV4"
#           } ] },
#   "status" : "success:created"
# }
# 201 Address created
# 404 Invalid asset specified
def ipaddress_allocate(asset, address_pool, count=1):
  logger.debug("Allocating %i addresses for %s in pool %s" % (count, asset.tag, address_pool))
  parameters = {
    'count' : count,
    'pool' : address_pool
  }
  r = http_handler.http_put("/api/asset/%s/address" % asset.tag, parameters, asset.location) 
  #for i in r:
  #  json_blob = parse_response(response, 'expects' : 201', 'default' : None)
  #  for t in json_blob:
  #    Address.from_json(t["data"]["ADDRESSES"])

# 200 Address updated
def ipaddress_update(asset, old_address=None, options=None):
  #logger.debug("Updating IP address for %s")
  parameters = {
    'old_address' : old_address,
    'address' : get_option(address, options, None),
    'gateway' : get_option(gateway, options, None),
    'netmask' : get_option(netmask, options, None),
    'pool' : get_option(pool, options, None)
  }
  parameters = params.select_non_empty_parameters(parameters)
  r = http_handler.http_post("/api/asset/%s/address" % asset.tag, parameters, asset.location)
  print r.text
    #parse_response(response, 'expects' : [200,201], 'default' : fal'se, 'raise' : str'ict?)

def ipaddress_delete(asset, pool=None):
  #logger.debug("Deleting addresses for asset %s in pool #{pool}")
  parameters = {
    'pool' : pool
  }
  parameters = params.select_non_empty_parameters(parameters)
  r = http_handler.http_delete("/api/asset/%s/addresses" % asset.tag, parameters, asset.location)
  print r.text
    #parse_response(response, 'expects' : 200', 'default' : fal'se, 'raise' : str'ict? do |json|)
      #json["data"]["DELETED"].to_s.to_i

def ipaddress_pools(show_all=True):
  #logger.debug("Finding IP address pools")
  r = http_handler.http_get("/api/address/pools", {'all' : show_all})
  print r.text
    #parse_response(response, 'expects' : 200', 'default' : [],' 'raise' : str'ict? do |json|)
      #json["data"]["POOLS"]

# {
#    "status":"success:ok",
#    "data":{
#       "ADDRESSES":[
#          {
#             "ASSET_ID":2,
#             "ASSET_TAG":"abc",
#             "GATEWAY":"10.25.0.1",
#             "ADDRESS":"10.25.0.2",
#             "NETMASK":"255.255.254.0",
#             "POOL":"SJ-MGMT-IPV4",
#             "ID":1
#          },
#          {
#             "ASSET_ID":2,
#             "ASSET_TAG":"abc",
#             "GATEWAY":"10.25.0.1",
#             "ADDRESS":"10.25.0.3",
#             "NETMASK":"255.255.254.0",
#             "POOL":"SJ-MGMT-IPV4",
#             "ID":3
#          }
#       ]
#    }
# }
def addresses_for_asset(asset):
  #logger.debug("Getting IP addresses for asset %s")
  r = http_handler.http_get("/api/asset/%s/addresses" % asset.tag, {}, asset.location)
  print r.text
    #parse_response(response, 'expects' : 200', 'default' : [],' 'raise' : str'ict? do |json|)
      #Collins::Address.from_json(json["data"]["ADDRESSES"])


def asset_at_address(address):
  #logger.debug("Finding asset at address #{address}")
  r = http_handler.http_get("/api/asset/with/address/%s" % address)
  print r.text
    #parse_response(response, 'expects' : 200', 'default' : None', 'raise' : str'ict?, 'as' : 'ba're_asset))

def assets_in_pool(pool):
  #logger.debug("Finding assets in pool #{pool}")
  r = http_handler.http_get("/api/assets/with/addresses/in/%s" % pool)
  print r.text
    #parse_response(response, 'expects' : 200', 'default' : [],' 'raise' : str'ict? do |json|)
      #json["data"]["ASSETS"].map{|j| Collins':Asset.from_json(j, true)}


if __name__ == "__main__":
  pass

  