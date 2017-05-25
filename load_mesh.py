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
import array
import os
import sys
from binascii import b2a_hex, a2b_hex

nova = 'GhostFemaleNova.m3'
nova = 'NovaEx1.m3'
nova = 'Storm_Hero_DVA_Base.m3'
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
vertices = []
triangles = []
divisions = []

for i in range(nm):
    item = struct.unpack_from('4slll', data[of:])
    of += 16

    tp = item[0][::-1]

    typeset.add(tp)

    m3item = (tp, item[1], item[2], item[3])
    m3items.append(m3item)

# decode MODL field
for i in m3items:
    if i[0] != 'MODL':
        continue

    vxRef = struct.unpack_from('l', data[i[1]+0x68:])[0]
    vxObj = m3items[vxRef]
    vFlag = struct.unpack_from('l', data[i[1]+0x60:])[0]

    vxSize = 32 # 0x182007d
    #vxSize = 36 if vFlag == 0x186007d else vxSize
    #vxSize = 40 if vFlag == 0x186027d else vxSize
    #vxSize = 44 if vFlag == 0x19e007d else vxSize

    #assert vFlag & 0x20000
    vxSize += 4 if vFlag & 0x200 else 0
    vxSize += 4 if vFlag & 0x40000 else 0
    vxSize += 4 if vFlag & 0x80000 else 0
    vxSize += 4 if vFlag & 0x100000 else 0

    for j in range(vxObj[2] / vxSize):
        (x, y, z) = struct.unpack_from('fff', data[vxObj[1]+j*vxSize:])
        #vertices.append((x, y, z, ))
        #print x, y, z
        vertices.append(x)
        vertices.append(z)
        vertices.append(y)
    print vxObj, 'vFlag: %x' % vFlag

print 'total vertices count:', len(vertices)

# decode DIV_ field
for div in m3items:
    if div[0] != 'DIV_':
        continue

    divSize = 52

    divOff = div[1]
    divLen = div[2]

    for i in range(divLen):
        (fo, fi, ff) = struct.unpack_from('lll', data[divOff+i*divSize:])
        #print fo, fi, ff

        faces = m3items[fi]
        fOff = faces[1]
        fLen = faces[2]

        if faces[0] != 'U16_':
            continue

        for i in range(fLen):
            (id, ) = struct.unpack_from('h', data[fOff+i*2:])
            triangles.append(id)

    print 'total triangles count:', len(triangles)

# decode BAT_ field
for i in m3items:
    if i[0] != 'BAT_':
        continue

    batSize = 14

    batOff = i[1]
    batLen = i[2]

    for i in range(batLen):
        (_, regionIndex, _, _materialRefIndex, _, ) = struct.unpack_from('lhlhh', data[batOff+i*batSize:])
        #print regionIndex, _materialRefIndex
        #print b2a_hex(data[batOff+i*14:batOff+i*14+14])
        # --> should call decode REGN here

# decode REGN field
for i in m3items:
    if i[0] != 'REGN':
        continue

    regSize = 36
    regSize = 40 if i[3] == 4 else regSize
    regSize = 48 if i[3] == 5 else regSize

    regOff = i[1]
    regLen = i[2]

    for i in range(regLen):
        (_, _, firstVertexIndex, numberOfVertices, ff, nff, fob, fb, nobli, _, nobwppv, _, rbi, _, _, ) = struct.unpack_from('llllllhhhhbbhl8s', data[regOff+i*regSize:])
        print 'div[%d]:' % i, firstVertexIndex, numberOfVertices, ff, nff
        divisions.append((firstVertexIndex, numberOfVertices, ff, nff, ))
