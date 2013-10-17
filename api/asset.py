
import http

# @param: [String] tumblrtag30
# @return status
def create_asset(asset):
  parameters = {
    "generate_ipmi":"false", 
    #"status":"Incomplete", 
    "status":"Unallocated", 
  #  "type":"SERVER_NODE", 
  }
  # TODO: logger - creating asset
  r = http_put("/asset/%s" % asset, parameters)
  print(r.text)

def delete_asset(asset):
  r = http_delete("/asset/%s" % asset)
  print(r.text)

def set_multi_attribute(asset, kv_hash):
  parameters = {
    'attribute': 'NODECLASS;py1234'
  }
  # TODO: logger - update asset
  r = http_post("/asset/%s" % asset, kv_hash)
  print(r.text)

def set_attribute(asset, key, value):
  set_multi_attribute (asset, {key : value})

def get_assets():
  print(http_get('/assets').text)


def main():
  create_asset()

if __name__ == "__main__":
  main()