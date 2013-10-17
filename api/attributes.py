#!/usr/bin/python

# bnguyen - bao@ooyala.com
# set sts=2


from pycollins.api.util import parameters as params
from pycollins.api.util import http_handler

def set_attribute(asset, key, value):
  r = set_multi_attribute(asset, {key : value})
  print(r.text)

def set_multi_attribute(asset, kv_hash, group_id=None):
  #TODO: impletement group_id for the second dimension of data
  parameters = {
    'groupId': group_id,
    'attribute': []
  }
  # TODO: logger - update asset
  for k,v in kv_hash.iteritems():
    if asset.is_not_attribute(k):
      parameters['attribute'].append(str(k) + ";" + str(v))
    else:
      p = asset.get_param(key)
      paramters[str(p)] = asset.get_param_value(key,value)
  #if not parameters['attribute']:
  #  parameters['attribute'] = None
  #elif len(parameters['attribute']) == 1:
  #  parameters['attribute'] = parameters['attribute'] # first values?
  #else:
  
  print parameters
  parameters = params.select_non_empty_parameters(parameters)
  
  # TODO: logger/log this action

  # parameters['http_options'] =  http_overrides if http_overrites else None #http_overwrite unless it's empty 
  # impletement asset.location?
  r = http_handler.http_post("/api/asset/%s" % asset.tag, parameters)
  # TODO: deal with response
  print(r.text)