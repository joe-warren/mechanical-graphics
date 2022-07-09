#!/usr/bin/env python3
import fontforge 
import string
import xml.etree.ElementTree as ET
from os.path import exists
from math import ceil
ns = {"svg": "http://www.w3.org/2000/svg"}

def filename(fontname, char):
    return f'{fontname}/{char}.svg'

def when_glyph_defined(font, fontname, char):
    f = filename(fontname, char)
    charSvg = ET.parse(f)
    svg =charSvg.getroot()
    height = float(svg.attrib['height'])
    width = float(svg.attrib['width'])
    # hacky workaround for fontforges svg scaling
    # scaling is based on the largest dimension
    # so before importing, set the total height to that
    # and then after, revert it to the actual height if that's smaller
    # any extra height gets added to the descender, as adding it to the 
    # ascent throws off the positioning 
    m = max(height, width)
    font.ascent = ceil(height * 10)
    font.descent = ceil((2*m - height) * 10)

    glyph = font.createChar(ord(char))
    glyph.width = ceil(width * 20)
    glyph.importOutlines(f, scale=True)
    glyph.width = ceil(width * 20)
   
    font.ascent = ceil(height * 10)
    font.descent = ceil(height * 10)

    print(f"{fontname} - {char} : {width} x {height}")
    print(glyph.boundingBox())

def build_font(fontname):
    font=fontforge.font()    
    chars = string.ascii_letters + string.digits + "&"
    
    for char in chars:
       if exists(filename(fontname, char)): 
           when_glyph_defined(font, fontname, char)
    dashed=fontname.replace(" ", "-").replace(".", "")
    font.familyname=f"Mechanical-Graphics-{dashed}"
    font.fontname=fontname.replace(" ", "_")
    font.fullname=f"Mechanical Graphics {fontname}"
    font.copyright="This font is in the public domain"
    font.save(f"output/{dashed}.sfd")  
    font.generate(f"output/{dashed}.ttf")
    print(f"finished {fontname}")

fonts = ["No. 1", "No. 2"]
for f in fonts:
    build_font(f)
