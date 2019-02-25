import sys
from xml.etree import ElementTree
import shutil
import os
import os.path
import json

html = ElementTree.Element("html")
body = ElementTree.Element("body")
html.append(body)

for dirpath, dirnames, filenames in os.walk("e:\Games\WindowsNoEditor\Evospace\Content\Generated\Mixed"):
	for filename in [f for f in filenames if f.endswith(".json")]:
		fullname = os.path.join(dirpath, filename)
		print fullname + " is parsing"
		
		with open(fullname) as f:
			data = json.load(f)
			
			for object in data["Objects"]:

				div = ElementTree.Element("div")
				body.append(div)
				span = ElementTree.Element("span")
				div.append(span)
				span.text = object["Name"]

string = ElementTree.tostring(html).decode()

file = open("Generated/Items.html","w+")
file.write(string)
file.close()
