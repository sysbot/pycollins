#!/usr/bin/python

# bnguyen - bao@ooyala.com
# set sts=2

import os
import os.path

# local
import requests
import yaml

# TODO: refactor code to run without using requests
# - making the DELETE avaiable for urllib2 [1]
# - code example [2] for making GET requests
# TODO: refactor code to use httplib, and example [3]

# [1] http://abhinandh.com/12/20/2010/making-http-delete-with-urllib2.html
# [2] https://gist.github.com/kennethreitz/973705
# [3] https://github.com/puppetlabs/Razor/wiki/Razor-API-Overview

# TODO: refactor YAML??

# logger code
import logging

logger = logging.getLogger("collins client")

def http_setup():
  session = requests.Session()
  home = os.getenv("HOME")
  with open(os.path.join(home, ".collins.yaml"), "r") as r:
    c = yaml.load(r)
    session.auth = (c['username'], c['password'])
    baseurl = c['host']
  return session, baseurl

def http_get(uri, parameters=None, remote=None):
  session, baseurl = http_setup()
  return session.get(baseurl + uri, data=parameters)

def http_put(uri, parameters=None, remote=None):
  session, baseurl = http_setup()
  return session.put(baseurl + uri, data=parameters)

def http_post(uri, parameters=None, remote=None):
  session, baseurl = http_setup()
  return session.post(baseurl + uri, data=parameters)

def http_delete(uri, parameters=None, remote=None):
  session, baseurl = http_setup()
  return session.delete(baseurl + uri)

if __name__ == "__main__":

  r = http_get('/api/asset/noc0-sjc1')
  print r.text
  print r.status_code