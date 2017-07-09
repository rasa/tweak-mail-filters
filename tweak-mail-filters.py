import pprint
import re
import sys
import xml.etree.ElementTree as ElementTree

INFILE = 'mailfilters.xml'
OUTFILE = 'newmailfilters.xml'
TEMP_XML = 'temp.xml'
TEMP2_XML = 'temp2.xml'

with open(INFILE, 'rb') as f:
	xml = f.read()

ns = {
	'': 'http://www.w3.org/2005/Atom',
	'apps': 'http://schemas.google.com/apps/2006'
}

map = [
	['<apps:property', '<property']
]

for k, v in ns.items():
	#ElementTree.register_namespace(k, v)
	vx = re.escape(v)
	if len(k) > 0:
		k = ':' + k
	s = "xmlns%s='%s'" % (k, v)
	c = 'x' + s
	#map.append([s, c])
	
map.append(
["<feed xmlns='http://www.w3.org/2005/Atom' xmlns:apps='http://schemas.google.com/apps/2006'>", "<feed>"]
)

for a in map:
	s = re.escape(a[0])
	xml = re.sub(a[0], a[1], xml)
	
with open(TEMP_XML, 'wb') as f:
	f.write(xml)

et = ElementTree.parse(TEMP_XML)

ENTRY = 'entry'
PROPERTY = 'property'
entries = et.findall(ENTRY)
for entry in entries:
	trash = False
	properties = entry.findall(PROPERTY)
	for property in properties:
		if 'name' in property.attrib:
			if property.get('name') == 'shouldTrash' and property.get('value') == 'true':
				trash = True

	for property in properties:
		if 'name' in property.attrib:
			if property.get('name') == 'label' and property.get('value') == 'auto-deleted':
				trash = False
				
	if trash:
		new_tag = ElementTree.SubElement(entry, PROPERTY)
		new_tag.attrib['name'] = 'label'
		new_tag.attrib['value'] = 'auto-deleted'
		
et.write(TEMP2_XML)

with open(TEMP2_XML, 'rb') as f:
	xml = f.read()

for a in map:
	s = re.escape(a[1])
	xml = re.sub(s, a[0], xml)

with open(OUTFILE, 'wb') as f:
	f.write(xml)

sys.exit(0)
