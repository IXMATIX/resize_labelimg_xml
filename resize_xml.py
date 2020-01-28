#!/usr/bin/python3

import os
import sys
import glob
import xml.etree.ElementTree as ET

scale = 1.0
if len(sys.argv) == 2:
    scale = float(sys.argv[1])
print("Scale: ", scale)

for xml_file in glob.glob('*.xml'):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    filename = root.find('filename')
    words = filename.text.split('.')
    filename.text = words[0] + ".jpg"

    path = root.find('path')
    words = path.text.split('.')
    path.text = words[0] + ".jpg"
    
    print("File: " + xml_file + " | " + filename.text + " Status: Resizing...")

    size = root.find('size')
    print("Old size: " + size[0].text + "x" + size[1].text)
    for i in range(2):
        size[i].text = str( int( float(size[i].text) * scale ) )
    print("New size: " + size[0].text + "x" + size[1].text)
    
    for obj in root.findall('object'):
        box = obj[4]
        for i in range(4):
            box[i].text = str( int( float(box[i].text) * scale ) )
    
    tree.write(xml_file)
    print("File: " + xml_file + " Status: OK!")