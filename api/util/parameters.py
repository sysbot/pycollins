#!/usr/bin/python

# bnguyen - bao@ooyala.com
# set sts=2

# select parameters from a values matching some options
def select_non_empty_parameters(params):
  return select_parameters(params, none_type=False, empty_string=False)

def select_parameters(params, **kwargs):
  x = {}
  for k, v in params.iteritems():
    #print (k,v)
    if v is None and kwargs['none_type'] == False:
      pass
    elif isinstance(v,basestring) and not v and kwargs['empty_string'] == False:
      pass
    else:
      x[k] = v
  return x

def get_option(key, blob, default):
  if key in blob:
    return blob[key]
  elif str(key) in blob:
    blob[str(key)]
  else:
    return default

def get_page_options(options=None):
  return {
    page: get_option(page, options, 0),
    size: get_option(size, options, 25),
    sort: get_option(sort, options, "DESC")
  }