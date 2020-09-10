#!/usr/bin/python3

import cv2
import glob
import os
import sys
import xml.etree.ElementTree as ET

# Set 1024 as default pixels value
max_pixels = 1024
# Default applied only if there's just one argument
if len(sys.argv) == 2:
    max_pixels = int(sys.argv[1])
# Show the destination pixels value
print("Max pixels: ", max_pixels)

# Iterate over all XML files in this relative folder
for xml_file in glob.glob("*.xml"):
    # Get XML tree from XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Get filename element from root
    filename = root.find("filename")
    # Get size element from root
    size = root.find("size")

    # Parse from STRING to INT width and height values
    width = int(size[0].text)
    height = int(size[1].text)

    # Show XML filename and image linked
    print("File:         ", xml_file)
    print("Image:        ", filename.text)

    # Define which side is larger to ensure max_pixels
    largest_side = width
    if height > width:
        largest_side = height
    print("Largest side: ", largest_side)

    # Check if a resize is applicable by evaluate if the
    # largest side is larger than max_pixels. Otherwise
    # the image is smaller than max_pixels
    resizable = largest_side > max_pixels
    print("Resizable:    ", resizable)

    # If resize isn't applicable skip to next XML file
    if not resizable:
        print("Status:       Skipping...")
        print("\n---------------------------------\n")
        continue
    # Else continue to resizing
    print("Status:       Resizing...")

    # Define scale variable to be calculated
    scale = 1.0
    # Check which side is the largest to calculate scale
    # Set the new largest side to max_pixels

    if largest_side == width:
        new_width = max_pixels
    # To calculate scale value divide max_pixels by old
    # pixels value, then multiplicate scale by other side
    # pixels and get its new value.
        scale = max_pixels / width
        new_height = int( height * scale )
    else:
        new_height = max_pixels
        scale = max_pixels / height
        new_width = int( width * scale )

    # Show old size vs new size as comparison
    print("Old size:     " + str(width) + "x" + str(height) \
        + "Total pixels: " + str(width*height) )
    print("New size:     " + str(new_width) + "x" + str(new_height) \
        + "Total pixels: " + str(new_width*new_height) )

    # Open image with OpenCV
    image = cv2.imread(filename.text)

    # Resize image with OpenCV
    image = cv2.resize(image, (new_width, new_height))

    # Save image with new size
    cv2.imwrite(filename.text, image)

    # Set new size in XML elements as STRING value
    size[0].text = str(new_width)
    size[1].text = str(new_height)
    
    # Get all OBJ/labels tags from root
    for obj in root.findall("object"):
        box = obj[4]
        # Scale each point in OBJ/label tag to hold its
        # original position relative to the new size
        for i in range(4):
            # Parse STRING to FLOAT to scale, then round with INT
            # and finally write into XML tree as STRING
            box[i].text = str( int( float(box[i].text) * scale ) )
    
    # Save changes into XML file and show status as OK!
    tree.write(xml_file)
    print("File:         " + xml_file)
    print("Status:       OK!")
    print("\n---------------------------------\n")