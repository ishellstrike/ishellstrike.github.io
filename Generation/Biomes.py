import sys
from xml.etree import ElementTree

html = ElementTree.Element("html")
body = ElementTree.Element("body")
html.append(body)
div = ElementTree.Element("div")
body.append(div)
span = ElementTree.Element("span")
div.append(span)
span.text = "Hello World"

string = ElementTree.tostring(html).decode()

file = open("Generated/Biomes.html","w+")
file.write(string)
file.close()