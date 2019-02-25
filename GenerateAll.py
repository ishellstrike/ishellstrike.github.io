import sys
from xml.etree import ElementTree
import subprocess
import shutil
import os
import os.path

our_path = os.path.dirname(sys.argv[0])

if os.path.isdir(our_path + "/Generated"):
	shutil.rmtree(our_path + "/Generated")

print our_path + "/Generated"
print "Cleanup..."	

for dirpath, dirnames, filenames in os.walk(our_path + "/Generation"):
	for filename in [f for f in filenames if f.endswith(".pyc")]:
		fullname = os.path.join(dirpath, filename)
		print fullname + " removed"
		os.remove(fullname)

print "Generation..."

os.makedirs("Generated")

for dirpath, dirnames, filenames in os.walk(our_path + "/Generation"):
	for filename in [f for f in filenames if f.endswith(".py")]:
		fullname = os.path.join(dirpath, filename)
		print fullname + " is runned"
		popen = subprocess.Popen("python " + fullname)
		popen.wait()
		print "Done"

html = ElementTree.Element("html")
body = ElementTree.Element("body")
html.append(body)
div = ElementTree.Element("div")
body.append(div)
span = ElementTree.Element("span")
div.append(span)
span.text = "Hello World"

L1div = ElementTree.Element("div")
L1 = ElementTree.Element("a", attrib={"href": "Generated/Items.html"}) 
L1div.append(L1)
body.append(L1div)
L1.text = "Items"

L2div = ElementTree.Element("div")
L2 = ElementTree.Element("a", attrib={"href": "Generated/Biomes.html"}) 
L2div.append(L2)
body.append(L2div)
L2.text = "Biomes"


string = ElementTree.tostring(html).decode()

file = open("index.html","w+")
file.write(string)
file.close()