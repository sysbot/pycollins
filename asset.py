#!/usr/bin/python

# bnguyen - bao@ooyala.com
# set sts=2


#import util
import dateutil.parser as parser
import json
import os.path
import copy
from api.util import parameters as params
from ipmi import IPMI
from address import Address

# Represents the basic notion of a collins asset
# Always use 'self' for the first argument to instance methods.
# Always use 'cls' for the first argument to class methods.
class Asset(object):
  # Default time format when displaying dates associated with an asset
  DATETIME_FORMAT = "%F %T"

  # Create an Asset
  # @param [Hash] kwargs Asset parameters
  # @option kwargs [String] tag The asset tag
  # @option kwargs [String] created The creation DateTime
  # @option kwargs [Fixnum] id The ID of the asset
  # @option kwargs [String] status The asset status
  # @option kwargs [String] type The asset type
  # @option kwargs [String] updated The update DateTime
  # @option kwargs [String] deleted The delete DateTime
  def __init__(self, *args, **kwargs):
    # @return [Collins::Ipmi] IPMI information

    # @return [String] multi-collins location
    #self.location
    # @return [Collins::Power] Power configuration information
    #self.power
    # @return [Collins::AssetState] Asset state, or None
    #self.state

    try:
      # assumed to alway have a dict
      self.tag = args[0]
    except KeyError:
      print "TAG is required and missing"
  
    # turn into lower case
    result = {}
    for k,v in kwargs.iteritems():
      t = k.lower()
      result[k] = v

    self.id = result.pop('id', '')
    self.created = self.parse_datetime(result.pop('created', ''))
    self.updated = self.parse_datetime(result.pop('updated', ''))
    self.deleted = self.parse_datetime(result.pop('deleted', '')) 
    self.status = result.pop('status','unallocated')
    self.type = result.pop('type', 'server_chassis')
    #self.state = CollinsAssetState.from_json(result.pop('state'))    
    self.state = "empty"
    
    # addresses
    self.addresses = []

    # TODO: implement location for multi-collins master servers
    self.location = ""

    # store extras in extras!
    self.extras = {}
    for k,v in result.iteritems():
      self.extras[k] = v

  def __str__(self):
    return "%s" % self.tag

  # how to import json into a predefined object/class?
  # metaclass, a class of an existing object instance (not part of the original class definition)
  # accessing metaclass directly is accessing self
  @classmethod
  def from_json(cls, json_blob):
    blob = copy.deepcopy(json_blob)

    json = blob.pop('data',blob)
    obj = json.pop('ASSET', json)

    result = {}
    for k,v in obj.iteritems():
      t = k.lower()
      result[t] = v
    
    a = cls(result['tag'], result)

    # set ipmi object
    a.ipmi = IPMI.from_json(json.pop('IPMI'))

    # set Address (IP Address)
    a.addresses = Address.from_json(json.pop('ADDRESSES'))

    return a

  def parse_datetime(self, s):
    if not s:
      return
    else:
      return parser.parse(s).isoformat()

  # @param 2013-06-11T00:31:32, "NEVER"
  # @return 2013-06-11T00:31:32 or "NEVER"
  def format_datetime(self, s, default="Never"):
    if not s:
      return default
    else:
      return s.strftime(DATETIME_FORMAT)    

  # # @return [Collins::Address,None] First available backend address
  def backend_address(self):
    if is_backend_address():
      return self.backend_addresses[0]

  # @return [Boolean] True if asset has a backend address
  def is_backend_address(self):
    if len(self.backend_addresses) > 0:
      return True
    else:
      return False

  # @return [List<Collins::Address>] List of backend addresses
  def backend_addresses(self):
    tmp = []
    for i in self.addresses:
      if i.is_private():
        tmp.append(i)
    self.backend_addresses = tmp

  # @return [String,None] Netmask of first available backend address
  def backend_netmask(self): 
    if is_backend_address():
      return self.backend_address.netmask

  # @return [List<String>] List of backend netmasks
  def backend_netmasks(self):
    tmp = []
    for i in self.addresses:
      if i.is_private:
        tmp.append(i)
    self.backend_netmasks = tmp

  # @return [Collins::Address,None] First available public address
  def public_address(self):
    if is_public_address():
      return public_addresses[0]

  # @return [Boolean] True if asset has a public address
  def is_public_address(self):
    if len(self.public_addresses) > 0:
      return True
    else:
      return False

  # @return [List<Collins::Address>] List of public addresses
  def public_addresses(self):
    tmp = []
    for i in self.addresses:
      if i.is_public:
        tmp.append(i)
    self.public_addresses = tmp

  # Return the gateway address for the specified pool, or the first gateway
  # @note If there is no address in the specified pool, the gateway of the first usable address is
  # used, which may not be desired.
  # @param [String] pool The address pool to find a gateway on
  # @return [String] Gateway address, or None
  def gateway_address(self, pool="default"):
    address = ""
    for i in self.addresses:
      if i.pool == pool:
        address = i.gateway

    # return the gateway if exist
    if address:
      return address

    # default, return the first address as the gateway
    if len(self.addresses) > 0:
      return addresses[0].gateway
    else:
      return None

  def set_attribute(self, key, value):
    r = self.set_multi_attribute({key : value})
    print(r.text)

  def set_multi_attribute(self, kv_hash):
    self.extras = kv_hash

  # @return [Object,None] See {#method_missing}
  def get_attribute(self, name):
    return extract(self.extras, "ATTRIBS", "0", str(name).upper())

  # @return [Fixnum] Number of CPU's found
  def cpu_count(self):
    return len(extract(self.extras, "HARDWARE", "CPU")) or None

  # @return [List<Hash>] CPU information
  def cpus(self):
    return extract(self.extras, "HARDWARE", "CPU") or None

  # @return [List<Hash>] Disk information
  def disks(self):
    return extract(self.extras, "HARDWARE", "DISK") or None

  # @return [List<Hash>] Memory information
  def memory(self):
    return extract(self.extras, "HARDWARE", "MEMORY") or None

  # @return [List<Hash>] NIC information
  def nics(self):
    return extract(self.extras, "HARDWARE", "NIC") or None

  # @return [Fixnum] Number of physical interfaces
  def physical_nic_count(self):
    return len(nics())

  # @return [List<String>] MAC addresses associated with assets
  def mac_addresses(self):
    t = []
    for k,v in nics.iteritems():
      t.append(k["MAC_ADDRESS"])

    return t

  # writing back to hash __str
  def to_json(self):
    tmp = {}
    #tmp['addresses'] = self.addresses
    #tmp['created'] = str(self.created)
    #tmp['updated'] = str(self.updated)
    #tmp['deleted'] = str(self.deleted)
    tmp['status'] = self.status
    tmp['tag'] = self.tag
    tmp['type'] = self.type
    #tmp['attribute'] = self.semicolon_attributes()
    r = json.dumps(tmp)
    #print r
    return r
    #state = CollinsAssetState.from_json(opts.pop('state'))    

  def semicolon_attributes(self):
    tmp = []
    for k,v in self.extras.iteritems():
      tmp.append("attribute=" + str(k) + ";" + str(v))
    return tmp

  # @return [String] Human readable asset with no meta attributes
  def __str__(self):
    #updated_t = format_datetime(updated, "Never")
    #created_t = format_datetime(created, "Never")
    #ipmi_i = "No IPMI Data" if ipmi is None
    if not self.ipmi:
      self.ipmi = "No IPMI Data"

    return "Asset(id = %s, tag = %s, status = %s,type = %s, created = %s, updated = %s, ipmi = %s, state = %s)" % (self.id, self.tag, self.status, self.type, self.created, self.updated, self.ipmi, self.state)

  def respond_to(self, name):
    if not extract(self.extras, "ATTRIBS", "0", str(name).upper()):
      super
    else:
      True

  # method for finding something in a (potentially) deep hash
  # @example
  #   a = '{"ATTRIBS": {"0": { "CHASSIS_TAG": "chassistag555",  "DISK_STORAGE_TOTAL": "24004743856128", "NODECLASS": "web;hadoop", "LINK1": "13" }}}''
  #   >>> extract(a,"ATTRIBS","0", "LINK1")
  #   '13'
  def extract(self, kv_hash, *args):
    try:
      tmp = kv_hash
      for i in args:
        tmp = tmp[i]
      return tmp
    except KeyError:
      return None  

  # ASSET CLASS FIND SECTION

  # Find API parameters that are dates
  # @return [Array<String>] Date related query parameters
  DATE_PARAMS = [ "createdAfter", "createdBefore", "updatedAfter", "updatedBefore"]
  
  # Find API parameters that are not dates
  # This list exists so that when assets are being queries, we know what keys in the find hash
  # are attributes of the asset (such as hostname), and which are nort (such as sort or page).
  # @return [Array,<String>] Non-date related query parameters that are 'reserved'
  GENERAL_PARAMS = [
    "details", "tag", "type", "status", "page", "size", "sort", "state", "operation", "remoteLookup", "query",
    "sortField"
  ]
  # @return [Array<String>] DATE_PARAMS plus GENERAL_PARAMS
  # ALL_PARAMS = DATE_PARAMS + GENERAL_PARAMS
  # class << self
  #   def to_a
  #     Collins::Asset::Find::ALL_PARAMS
  #   end
  #   def valid? key
  #     to_a.include?(key.to_s)

  # ASSET CLASS UPDATE SECTION
  NON_ATTRIBUTE_PARAMS = ["CHASSIS_TAG", "RACK_POSITION", "/^POWER_(.*)_(.*)/i"]
  FILE_PARAMS = ["lshw", "lldp"]
  ALL_PARAMS = NON_ATTRIBUTE_PARAMS + FILE_PARAMS

  def to_a(self):
    return self.ALL_PARAMS

  def get_param_value(self, key, value):
    if self.is_file_param(key):
      if value.start_with('@'):
        filename = os.path.abspath(value.replace('@',''))
        try:
          with open(filename): pass
        except IOError:
          print 'File does not exist.'
      else:
        value
    else:
      value

  # get_param_value
  def get_param(self, key):
    for k in self.to_a():
      if k == key:
        # Assume it's a power setting until we have >1 regexp
        return key.upper()
      elif str(key).upper() == str(k).upper():
        return k
    return key # get_param

  def is_file_param(self, key):
    # compact code for checking this!!
    #map(lambda x:x.lower(),FILE_PARAMS) include?(str(key).upper) # is_file_param?
    # FILE_PARAMS.map{|k|str(k).upper}.include?(str(key).upper)
    for i in self.ALL_PARAMS:
      if key.lower() == i.lower():
        return True
      else:
        return False

  def is_not_attribute(self, key):
    for k in self.to_a():
      if k == key:
        return False
      elif str(key).upper() == str(k).upper():
        return False
    return True


if __name__ == "__main__":
  # "data": {
  #     "ASSET": [], 
  #     "HARDWARE": [], 
  #     "LLDP": [], 
  #     "IPMI": [], 
  #     "ADDRESSES": [ ], 
  #     "POWER": [ ], 
  #     "ATTRIBS": []
  #     }
  # }
  #a = Asset(tag='ee')
  #print a

  t = {"data": { "ASSET": {'TAG':'ee2'}, "HARDWARE": '', "LLDP": '', "IPMI": { "ASSET_ID": 22, 
            "ASSET_TAG": "e1234", 
            "IPMI_USERNAME": "root", 
            "IPMI_PASSWORD": "n3Glgc8lVstp", 
            "IPMI_GATEWAY": "10.0.0.1", 
            "IPMI_ADDRESS": "10.0.0.15", 
            "IPMI_NETMASK": "255.255.0.0", 
            "ID": 14}, "ADDRESSES": '', "POWER": '',"ATTRIBS": ''}}

  b = Asset.from_json(t)
  print b

  print b.ipmi