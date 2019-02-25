import sys
from xml.etree import ElementTree

html = ElementTree.Element('html')
body = ElementTree.Element('body')
html.append(body)
div = ElementTree.Element('div', attrib={'class': 'foo'})
body.append(div)
span = ElementTree.Element('span', attrib={'class': 'bar'})
div.append(span)
span.text = "Hello World"


string = ElementTree.tostring(html).decode()

file = open("index.html","w+")
file.write(string)
file.close()

#e:\Games\WindowsNoEditor\Evospace\Content\Generated\Mixed