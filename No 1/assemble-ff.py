#!/usr/bin/env python3
import fontforge 
import string

font=fontforge.font()    

chars = string.ascii_letters + string.digits + "&"

for l in chars:
    glyph = font.createChar(ord(l))
    glyph.importOutlines('%s.svg' % l)

font.fontname="Mechanical Graphics No 1"
font.fullname="Mechanical Graphics No 1"
font.save("NewFont.sfd")  
font.generate("No-1.ttf")
print("done")
