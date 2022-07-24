#!/usr/bin/env python3
import fontforge 
import string
import xml.etree.ElementTree as ET
import os
from os.path import exists
from math import ceil
import re
ns = {"svg": "http://www.w3.org/2000/svg"}

def filename(fontname, char, weight=None):
    if weight == None:
       return f'{fontname}/{char}.svg'
    else:
       return f'{fontname}/{char}-{weight}.svg'
def when_glyph_defined(font, fontname, char, weight):
    f = filename(fontname, char, weight)
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

def get_weights(fontname):
  files = os.listdir(fontname) 
  r = re.compile("^.-([A-z]*)\.svg$")
  
  variants = set(r.match(f).group(1) for f in files if r.match(f)) 
  variants.add("Regular")
  return variants

def build_weighted_font(fontname, weight=None):
    font=fontforge.font()    
    chars = string.ascii_letters + string.digits + "&"
    
    for char in chars:
       if exists(filename(fontname, char, weight)): 
           when_glyph_defined(font, fontname, char, weight)
       elif exists(filename(fontname, char)): 
           when_glyph_defined(font, fontname, char, None)
    dashed=fontname.replace(" ", "-").replace(".", "")
    font.fontname=fontname.replace(" ", "_")
    font.fullname=f"Mechanical Graphics {fontname}"
    font.copyright="This font is in the public domain"
    name = dashed
    if weight == None:
        font.weight = "Regular"
    else:
        font.weight = weight
        name = f"{dashed}-{weight}"

    font.familyname=f"Mechanical-Graphics-{name}"
    font.save(f"output/{name}.sfd")  
    font.generate(f"output/{name}.ttf")
    print(f"finished {fontname}")

def build_font(fontname):
    weights = get_weights(fontname)
    if(len(weights) == 1):
      build_weighted_font(fontname)
    else:
      for weight in get_weights(fontname):
        build_weighted_font(fontname, weight)
fonts = ["No. 1", "No. 2", "No. 3", "No. 4", "No. 5", "No. 6", "No. 7", "No. 8"]
for f in fonts:
    build_font(f)
