import xml.etree.ElementTree as ET


tree = ET.parse('country_data.xml')
root = tree.getroot()
ff = root.findall(".//*[@name='Singapore']/year")

print ff[0].text