import sys
from xml.etree import ElementTree
import shutil
import os
import os.path
import json

from PIL import Image

html = ElementTree.Element("html")
body = ElementTree.Element("body")
html.append(body)

def lerp(x, y, a):
	return x+(y-x)*a

for dirpath, dirnames, filenames in os.walk("e:\Games\WindowsNoEditor\Evospace\Content\Generated\Mixed"):
	for filename in [f for f in filenames if f.endswith(".json")]:
		fullname = os.path.join(dirpath, filename)
		print fullname + " is parsing"
		
		with open(fullname) as f:
			data = json.load(f)

			for object in data["Objects"]:
			
				if object["Class"] == "SolidStaticItem" or object["Class"] == "FluidStaticItem" or object["Class"] == "EnergyStaticItem":  
				
					div = ElementTree.Element("div")
					body.append(div)
					span = ElementTree.Element("span")
					div.append(span)
					span.text = object["Name"]
					
					img = ElementTree.Element("img", attrib={"src": "Items/" + object["Image"] + ".png"})
					div.append(img)
					
string = ElementTree.tostring(html).decode()

file = open("Generated/Items.html","w+")
file.write(string)
file.close()

for dirpath, dirnames, filenames in os.walk("e:\Games\WindowsNoEditor\Evospace\Content\Generated\Resources"):
	for filename in [f for f in filenames if f.endswith(".json")]:
		fullname = os.path.join(dirpath, filename)
		print fullname + " is parsing"
		
		with open(fullname) as f:
			data = json.load(f)

			for object in data["Objects"]:
			
				if object["Class"] == "IcoGenerator":  
				
					for image in object["Images"]:
					
						try:
							img = Image.new("RGBA", (32,32), (255,255,255,0))
							output = img.load()
						
							ibase = Image.open("Source/" + image["Base"] + ".tga")
							pixels = ibase.load()
							
							if "MulMask" in image:
								mbase = Image.open("Source/" + image["MulMask"] + ".tga")
								mpixels = mbase.load()
								for i in range(img.size[0]):
									for j in range(img.size[1]):
										color = tuple(int((l / 255.0) * (r / 255.0) * 255) for l, r in zip(pixels[i, j], mpixels[i, j]))
										output[i, j] = (color[0], color[1], color[2], pixels[i, j][3])
										
							if "AddMask" in image:
								try:
									if isinstance(image["AddMask"], list):
										for addmask in image["AddMask"]:
											mbase = Image.open("Source/" + addmask + ".tga")
											mpixels = mbase.load()
											for i in range(img.size[0]):
												for j in range(img.size[1]):
													r = int(lerp(output[i, j][0], mpixels[i, j][0], mpixels[i, j][3] / 255.0))
													g = int(lerp(output[i, j][1], mpixels[i, j][1], mpixels[i, j][3] / 255.0))
													b = int(lerp(output[i, j][2], mpixels[i, j][2], mpixels[i, j][3] / 255.0))
													a = max(output[i, j][3], mpixels[i, j][3])
													
													output[i, j] = (r, g, b, a)
									else:
										mbase = Image.open("Source/" + image["AddMask"] + ".tga")
										mpixels = mbase.load()
										for i in range(img.size[0]):
											for j in range(img.size[1]):
												r = int(lerp(output[i, j][0], mpixels[i, j][0], mpixels[i, j][3] / 255.0))
												g = int(lerp(output[i, j][1], mpixels[i, j][1], mpixels[i, j][3] / 255.0))
												b = int(lerp(output[i, j][2], mpixels[i, j][2], mpixels[i, j][3] / 255.0))
												a = max(output[i, j][3], mpixels[i, j][3])
												
												output[i, j] = (r, g, b, a)
								except IOError:
									None
							
							img.save("Generated/Items/" + image["NewName"] + ".png")
						except IOError:
							print image["NewName"] + " err" + str(IOError)

for dirpath, dirnames, filenames in os.walk("Source"):
	for filename in [f for f in filenames if f.endswith(".TGA")]:
		fullname = os.path.join(dirpath, filename)
		img = Image.open(fullname)
		name = "Generated/Items/" + os.path.splitext(filename)[0] + ".png"
		img.save(name)
			
recipe_index = 0			

html = ElementTree.Element("html")
body = ElementTree.Element("body")
html.append(body)

recipe_index = 0

for dirpath, dirnames, filenames in os.walk("e:\Games\WindowsNoEditor\Evospace\Content\Generated\Recipes"):
	for filename in [f for f in filenames if f.endswith(".json")]:
		fullname = os.path.join(dirpath, filename)
		print fullname + " is parsing"
		
		with open(fullname) as f:
			data = json.load(f)
		
			for object in data["Objects"]:
				if object["Class"] == "BaseRecipeDictionary":
					for recipe in object["Recipes"]:
						
						div = ElementTree.Element("div")
						body.append(div)
						span = ElementTree.Element("span")
						div.append(span)
						span.text = object["Name"]
						
						for inp in recipe["Input"]["Items"]:
							iconame = inp["Name"].replace("StaticItem", "Ico.png")						
							img = ElementTree.Element("img", attrib={"src": "Items/" + iconame})
							div.append(img)
							span = ElementTree.Element("span")
							span.text = str(inp["Count"])
							div.append(span)
							
						span = ElementTree.Element("span")
						div.append(span)
						span.text = " -> "
							
						for inp in recipe["Output"]["Items"]:
							iconame = inp["Name"].replace("StaticItem", "Ico.png")						
							img = ElementTree.Element("img", attrib={"src": "Items/" + iconame})
							div.append(img)
							span = ElementTree.Element("span")
							span.text = str(inp["Count"])
							div.append(span)
						
						recipe_index = recipe_index + 1
					
string = ElementTree.tostring(html).decode()

file = open("Generated/Recipes.html","w+")
file.write(string)
file.close()