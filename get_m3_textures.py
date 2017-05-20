#!/bin/env python
# -*- coding: utf-8 -*-

#
# read a Starcraft II m3/m3a file, print out all textures it needs
# just available for the current version (sc2 3.13.0.52910)
#
# maybe i need a GUI and associate .m3 & .m3a in registry for convenience
#

import hashlib
import struct
import os
import sys
from binascii import b2a_hex, a2b_hex

nova = 'GhostFemaleNova.m3'
#nova = 'GhostFemale_RequiredAnims.m3a'

data = open(nova, 'rb').read()

head = struct.unpack('4sllll', data[:20])
of = head[1]
nm = head[2]

typeset = set()
m3items = []

for i in range(nm):
    item = struct.unpack('4slll', data[of:of+16])
    of += 16

    tp = item[0][::-1]

    #print '%2d' % i, tp, item

    typeset.add(tp)

    m3item = (tp, item[1], item[2], item[3])
    m3items.append(m3item)

#print typeset
#print len(data), of
#print struct.unpack('4slllll', data[:24])

def getString(i):
    item = m3items[i]
    assert item[0] == 'CHAR'
    assert item[2] > 0

    return data[item[1]:item[1]+item[2]-1]

def decodeMatLayer(mdata):
    imagePathLen = struct.unpack('l', mdata[0x4:0x4+4])[0]
    imagePathRef = struct.unpack('l', mdata[0x8:0x8+4])[0]
    if imagePathLen > 0:
        return getString(imagePathRef)

textures = set()

for i in m3items:
    if i[0] == 'LAYR':
        assert i[2] == 1
        assert i[3] == 26
        imagePath = decodeMatLayer(data[i[1]:i[1]+464])
        if imagePath:
            textures.add(imagePath)

for i in textures:
    print i
