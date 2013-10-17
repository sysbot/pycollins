# pycollins

This is Python implementation of Collins Client SDK [1] There still lots of 
refactoring and tests that needed to do. It's a start to get going but if you 
want production quality code, use the Ruby SDK gems from Tumblr instead [2]]

# Setup


# Example

Basica examples to use the client code

	# local
	from pycollins.asset import Asset
	from pycollins.asset import AssetClient
	from pycollins.client import Client
	from pycollins.api.util import parameters as params

	tag = "servername"
    client.create_asset(tag)
    client.update_ipmi(i)
    ipaddress.ipaddress_allocate(i,"poolname")
    ipaddress.ipaddress_allocate(i,"loopback0")

# References

[1] http://tumblr.github.io/collins/api.html
[2] https://rubygems.org/gems/collins_client
