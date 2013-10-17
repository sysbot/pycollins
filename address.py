#!/usr/bin/python

# bnguyen - bao@ooyala.com
# set sts=2

import ipaddress

from api import ip_address

class Address(object):
  # alternative constructor with deserialized json
  @classmethod
  def from_json(cls, json_blob):
    if not json_blob:
      return None
 
    addresses = []
    for i in json_blob:
      addresses.append(cls(i))
    return addresses

  def __init__(self, model):
    result={}
    for k,v in model.iteritems():
      t = k.lower()
      result[t] = v

    self.id = str(result.pop('id', ''))
    self.asset_id = str(result.pop('asset_id', ''))    
    self.address = str(result.pop('address', ''))
    self.gateway = str(result.pop('gateway', ''))
    self.netmask = str(result.pop('netmask', ''))
    self.pool = str(result.pop('pool', ''))
    self.ip = ipaddress.IPv4Address(unicode(self.address))

  def is_addressable(self):
    return self.ip.version == 4

  def is_private(self):
    return self.ip.is_private

  def is_public(self):
    return not self.ip.is_private

  def __str__(self):
    return "Collins::Address(address = %s, gateway = %s, netmask = %s, is_private = %s)" % (self.address, self.gateway, self.netmask, self.is_private())

if __name__ == "__main__":

  from asset import Asset

  t =  {
    "ADDRESSES":[
       {
          #"ASSET_ID":6,
          #"ASSET_TAG":"noc0-sjc1",
          "GATEWAY":"10.25.248.1",
          "ADDRESS":"10.25.249.2",
          "NETMASK":"255.255.254.0",
          "POOL":"SJ-LOOPBACK2-IPV4",
          #"ID":1
       },
       {
          #"ASSET_ID":6,
          #"ASSET_TAG":"noc0-sjc1",
          "GATEWAY":"10.25.248.1",
          "ADDRESS":"10.25.249.3",
          "NETMASK":"255.255.254.0",
          "POOL":"SJ-LOOPBACK2-IPV4",
          #"ID":3
       }
    ]
  }
  #a = IPMI()
  #print a

  a = Asset("noc0-sjc1")

  b = Address.from_json(t['ADDRESSES'])
  for i in b:
    print i
    ip_address.ipaddress_pools()
    #ip_address.
    break

