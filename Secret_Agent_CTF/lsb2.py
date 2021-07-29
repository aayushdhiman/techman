# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 09:48:42 2021

@author: student
"""
img = 'C:\\Users\\student\\Desktop\\agent.png'

from PIL import Image
import bitstring

extracted_bin = []
with Image.open("C:\\Users\\student\\Desktop\\agent.png") as img:
    width, height = img.size
    for x in range(0, width):
        for y in range(0, height):
            pixel = list(img.getpixel((x, y)))
            for n in range(0,4):
                extracted_bin.append(pixel[n]&1)
                # print(pixel[n]&1)

data = "".join([str(x) for x in extracted_bin])

output = open("output.bin", "wb+")
output.write((bitstring.BitArray(bin=data)).tobytes())


        
