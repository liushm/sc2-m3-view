#!/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as xtree

keyG = [0, 0]
key = [[0, 0, 0, 0] for i in range(10)]

valueG = [0, 0]
result = [0] * 10

if True:
    keyG[0] = 'IllllIllllIlIlII'
    keyG[1] = 'lllIlllIIlIlIlll'

    key[0][0] = 'lllIIlllIIIIIlII'
    key[0][1] = 'lIlIlllllIIIlllI'
    key[0][2] = 'lIlIIIIlllIlIlll'
    key[0][3] = 'lIlIIlIIIllIllIl'
    key[1][0] = 'lllIIIllllIIIIII'
    key[1][1] = 'IIlIlllIIlllllll'
    key[1][2] = 'lllllIllIIlIllll'
    key[1][3] = 'lIIlIIIlIIIIIllI'
    key[2][0] = 'IlIIlIIllIlIIIll'
    key[2][1] = 'llIllllllllllllI'
    key[2][2] = 'lIlIIlllIlIllIll'
    key[2][3] = 'IlllIlIllllIllII'
    key[3][0] = 'IlIlIIlllIllllIl'
    key[3][1] = 'IIlIIllIllllIIll'
    key[3][2] = 'IIIlIIlIIlllllII'
    key[3][3] = 'lIlllIlIlllIllIl'
    key[4][0] = 'lllIlIIIllllllll'
    key[4][1] = 'lIlIIlIIllIIlllI'
    key[4][2] = 'IllIllllIIllIlIl'
    key[4][3] = 'llIIIlllIlllIIII'
    key[5][0] = 'lIllIIlllIIlIllI'
    key[5][1] = 'llIIllIllIIlIllI'
    key[5][2] = 'IIIIllllIIllllll'
    key[5][3] = 'lIlllllIIIlIlIIl'
    key[6][0] = 'lIIIlIIlIllIllIl'
    key[6][1] = 'lIIIIIIIIllllIIl'
    key[6][2] = 'IlIllIlIlllllllI'
    key[6][3] = 'lIlIIIIllllllIll'
    key[7][0] = 'llIIIlIlIIllllIl'
    key[7][1] = 'IllIIlIIlIllIIIl'
    key[7][2] = 'IIIIIlllIIIlllIl'
    key[7][3] = 'llllIIlIlIIlIIII'
    key[8][0] = 'IIllIlIIlIIllIII'
    key[8][1] = 'IIllllllllIlllII'
    key[8][2] = 'IIIIIlIllllIlIll'
    key[8][3] = 'llllIIlIllIIIlII'
    key[9][0] = 'lIlIllIIIIIlllIl'
    key[9][1] = 'IIllllIlllllIlII'
    key[9][2] = 'IlllIIlIIllIlIII'
    key[9][3] = 'lIIIIIllIIlIlIII'

#bank = xtree.parse('Starlight.SC2Bank')
bank = xtree.parse('C:/Users/terran/Documents/StarCraft II/Accounts/190020978/5-S2-1-1538329/Banks/5-S2-1-561377/Starlight.SC2Bank')
root = bank.getroot()

hero = root.find('Section[@name="HeroLineWar"]')

valueG[0] = int(hero.find('Key[@name="{}"]'.format(keyG[0]))[0].attrib['int'])
valueG[1] = int(hero.find('Key[@name="{}"]'.format(keyG[1]))[0].attrib['int'])

# print valueG[0], valueG[1]

# [经验, 游戏场次, 获胜, 消灭敌方单位, 生产数量, 已购物品, 已用消耗品, 最快胜利, 0, 0]

for i in range(10):
    a = int(hero.find('Key[@name="{}"]'.format(key[i][0]))[0].attrib['int'])
    b = int(hero.find('Key[@name="{}"]'.format(key[i][1]))[0].attrib['int'])
    c = int(hero.find('Key[@name="{}"]'.format(key[i][2]))[0].attrib['int'])
    d = int(hero.find('Key[@name="{}"]'.format(key[i][3]))[0].attrib['int'])

    result[i] = c - valueG[1] - (a - valueG[0])
    result[i] = d - valueG[0] - (b - valueG[1])

    print result[i]
