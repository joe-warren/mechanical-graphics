#!/usr/bin/env python3
import fontforge 
import string
import xml.etree.ElementTree as ET
ns = {"svg": "http://www.w3.org/2000/svg"}

font=fontforge.font()    

chars = string.ascii_letters + string.digits + "&"

for l in chars:

    charSvg = ET.parse('%s.svg' % l)
    print(charSvg)
    svg =charSvg.getroot() # charSvg.find(".//{http://www.w3.org/2000/svg}svg", ns)
    print(svg)

    font.ascent = int(svg.attrib["height"]) * 10
    font.descent = int(svg.attrib["height"]) * 10

    glyph = font.createChar(ord(l))
    glyph.importOutlines('%s.svg' % l)
    glyph.width = (int(svg.attrib["width"])) * 20 
    print(glyph.width)
    #glyph.autoHint()

font.familyname="Mechanical-Graphics-No-1"
font.fontname="No_1"
font.fullname="Mechanical Graphics No. 1"
font.copyright="This font is in the public domain"
font.save("NewFont.sfd")  
font.generate("No-1.ttf")
print("done")
