#!/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as xt

s = "GHKLMpvwxyzABCdefghijklmDEF345sIJtuN6789.-abcRSTUVOPQr12qon0WXYZ"
d = "qM5wyGHJdfghjkl8N2zxcXCVvbKLn3.QWop7ERui4sTYUm96IOP-AS10aDFertZB"
t = {}
n = {}
for i in range(len(s)):
    t[s[i]] = d[i]
    n[d[i]] = s[i]

def sb_str_encode(msg):
    ret = ''
    for i in msg:
        ret += t[i]

    ret = ret[::3] + ret[1::3] + ret[2::3]
    ret = ret[len(ret)/2:len(ret)] + ret[0:len(ret)/2]

    return ret

# all inventory list , bag & store

bag = []

def calculate_checkcode2():
    return sb_str_encode(''.join(bag))

# yeah, it's ok, since all parameters are integers
def calculate_checkcode(score, times, uid):
    code = str(12436 + score/10*9 + 49/12*11 - times/11*10 - 102548.375)

    return sb_str_encode(sb_str_encode(code) + uid)

bag.append('24SlotBag')
bag.append('24SlotBag')
bag.append('24SlotBag')
bag.append('24SlotBag')
bag.append('24SlotBag')
bag.append('PickupPlasmaGun32322')
bag.append('Excalibur')
bag.append('mjnszw')
bag.append('cxnxjq')
bag.append('jlfd')
bag.append('mkdxl4')
bag.append('yxxz5')
bag.append('kjgp')
bag.append('byph')
bag.append('sssh')
bag.append('yhsszy')
bag.append('yswdcj')
bag.append('jztsq')

szb2 = xt.Element('Section', {'name':'zhuangbei2'})

for i in range(len(bag)):
    k = xt.SubElement(szb2, 'Key', {'name':'{}'.format(i + 1)})
    v = xt.SubElement(k, 'Value', {'string':'{}'.format(bag[i])})

xt.dump(szb2)

print ''
print calculate_checkcode(39899, 671, '5-S2-1-1538329')
print calculate_checkcode2()





































