#from pycollins.util import parameters as params

class IPMI(object):

  # alternative constructor with deserialized json
  @classmethod
  def from_json(cls, json_blob):
    return cls(json_blob)

  def __init__(self, json_blob):

    result={}
    for k,v in json_blob.iteritems():
      t = k.lower()
      key = t.replace("ipmi_","")
      result[key] = v

    self.address = str(result.pop('address', ''))
    self.asset_id = str(result.pop('asset_id', ''))
    self.gateway = str(result.pop('gateway', ''))
    self.id = str(result.pop('id', ''))
    self.netmask = str(result.pop('netmask', ''))
    self.password = str(result.pop('password', ''))
    self.username = str(result.pop('username', ''))

  def empty(self):
    if self.address:
      return 0
    else:
      return 1

  def __str__(self):
    if self.empty():
      return "IPMI(None)"
    else:
      return "IPMI(id = %s, asset_id = %s, address = %s, gateway = %s, netmask = %s, username = %s, password = %s)" % (self.id, self.asset_id, self.address, self.gateway, self.netmask, self.username, self.password)


if __name__ == "__main__":
  # JSON FROM SERVER
  # "IPMI": {
  #     "ASSET_ID": 22, 
  #     "ASSET_TAG": "e1234", 
  #     "IPMI_USERNAME": "root", 
  #     "IPMI_PASSWORD": "n3Glgc8lVstp", 
  #     "IPMI_GATEWAY": "10.0.0.1", 
  #     "IPMI_ADDRESS": "10.0.0.15", 
  #     "IPMI_NETMASK": "255.255.0.0", 
  #     "ID": 14
  # }, 

  t =  { "ASSET_ID": 22, "ASSET_TAG": "e1234", "IPMI_USERNAME": "root", "IPMI_PASSWORD": "n3Glgc8lVstp", "IPMI_GATEWAY": "10.0.0.1", "IPMI_ADDRESS": "10.0.0.15", "IPMI_NETMASK": "255.255.0.0", "ID": 14 } 

  #a = IPMI()
  #print a

  b = IPMI.from_json(t)
  print b
