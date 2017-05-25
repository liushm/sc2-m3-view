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
#nova = 'Marine.m3'

data = open(nova, 'rb').read()

#
#refStruct -> (entries index flags)
#refStruct = struct.Struct('lll')

head = struct.unpack_from('4sllll', data)
of = head[1]
nm = head[2]

typeset = set()
m3items = []

for i in range(nm):
    item = struct.unpack_from('4slll', data[of:])
    of += 16

    tp = item[0][::-1]

    print '%2d' % i, tp, item, data[item[1]:item[1]+item[2]-1] if tp == 'CHAR' else ''

    typeset.add(tp)

    m3item = (tp, item[1], item[2], item[3])
    m3items.append(m3item)

print typeset
print len(data), of
print struct.unpack_from('4slllll', data)

def getString(i):
    item = m3items[i]
    assert item[0] == 'CHAR'
    assert item[2] > 0

    return data[item[1]:item[1]+item[2]-1]

def decodeMatLayer(mdata):
    imagePathLen = struct.unpack_from('l', mdata[0x4:])[0]
    imagePathRef = struct.unpack_from('l', mdata[0x8:])[0]
    if imagePathLen > 0:
        return getString(imagePathRef)

textures = set()

for i in m3items:
    if i[0] == 'LAYR':
        assert i[2] == 1
        #assert i[3] == 26
        imagePath = decodeMatLayer(data[i[1]:])
        if imagePath:
            textures.add(imagePath)
    elif i[0] == 'MODL':
        vxRef = struct.unpack_from('l', data[i[1]+0x68:])[0]
        vxObj = m3items[vxRef]
        vFlag = struct.unpack_from('l', data[i[1]+0x60:])[0]
        print vxObj
        print '%x' % vFlag
        for j in range(vxObj[2] / 32):
            (x, y, z) = struct.unpack_from('fff', data[vxObj[1]+j*32:])
            #print x, y, z

for i in textures:
    print i
