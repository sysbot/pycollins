#!/usr/bin/python

# bnguyen - bao@ooyala.com
# set sts=2

import unittest
from asset import Asset

TAG = "abc"

class AssetTestCase(unittest.TestCase):
  def setUp(self):
  	self.asset = Asset(TAG)

class DefaultAssetTestCase(AssetTestCase):
	def runTest(self):
		self.assertEqual(self.asset.tag, TAG, "something really wrong")

def main():
  unittest.main()

if __name__ == '__main__': 
  main()

