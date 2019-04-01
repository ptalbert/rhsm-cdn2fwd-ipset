#/bin/python
# BEGIN rhsm-cdn2fwd-ipset.py

import json, sys, urllib, xml.dom.minidom

method = 'file'

JSON_FILE= 'cdn_redhat_com_cac.json'
JSON_URL = 'https://access.redhat.com/sites/default/files/cdn_redhat_com_cac.json'

if method == 'file':
	try:
		with open(JSON_FILE, 'r') as jsonfile:
			data = json.load(jsonfile)
	except:
		print "Error importing JSON data from %s" % (JSON_FILE)
		sys.exit(1)
elif method == 'url':
	try:
		urldata = urllib.urlopen(JSON_URL)
		data = json.load(urldata)
	except:
		print "Error importing JSON data from %s" % (JSON_URL)
		sys.exit(1)

if 'version' not in data or len(data['cidr_list']) < 1:
	print ("JSON does not contain expected 'version' object "
		"or has an empty 'cidr_list'")
	sys.exit(1)

print ("Data version %s imported containing %d addresses ...\n"
	% (data['version'], len(data['cidr_list'])))

def newElement(doc, name, value):
	element = doc.createElement(name)
	text = doc.createTextNode(value)
	element.appendChild(text)
	return element

xmldoc = xml.dom.minidom.Document()
ipset = xmldoc.createElement("ipset")
ipset.setAttribute("type", "hash:ip")
xmldoc.appendChild(ipset)

short_element = newElement(xmldoc, "short", "Red Hat RHSM CDN")
ipset.appendChild(short_element)

description = ("Red Hat Subscription Manager Content Delivery Network"
		"Public IP addresses (version %s)" % data['version'])
description_element = newElement(xmldoc, "description", description)
ipset.appendChild(description_element)

for cidr_item in data['cidr_list']:
	entry = newElement(xmldoc, "entry", cidr_item['ip_prefix'])
	ipset.appendChild(entry)

print xmldoc.toprettyxml()

# END rhsm-cdn2fwd-ipset.py
