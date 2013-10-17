#!/usr/bin/python

# bnguyen - bao@ooyala.com
# set sts=2

from asset import Asset

# Convenience class for making collins calls for only a single asset
class AssetClient(object):
  def __init__(self, asset, client, logger):
    self.asset = asset
    if isinstance(asset, Asset):
      self.tag = asset.tag
    else:
      self.tag = asset
    self.client = client
    self.logger = logger

  def __str__():
    "AssetClient(asset = %s, client = %s)" % (self.tag, self.client)

if __name__ == "__main__":
  pass