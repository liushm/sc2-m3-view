#!/bin/env python

alphabet = {
    "\x31":"\x40", "\x32":"\x24", "\x33":"\x5E", "\x34":"\x2A", "\x35":"\x29",
    "\x36":"\x21", "\x37":"\x23", "\x38":"\x25", "\x39":"\x7E", "\x30":"\x28"
}
betabet = {}

for i in alphabet:
    betabet[alphabet[i]] = i

def str2num(msg):
    ret = ''
    for i in msg:
        ret += betabet[i]
    return ret

def num2str(num):
    ret = ''
    for i in num:
        ret += alphabet[i]
    return ret

def calculate_vc(xp, c, d, m, s, handle):
    ret = 0

    ret += (xp + 159)
    ret += (c + 99)
    ret += (d * 15)
    ret += (m * 13)
    ret += (s + 175)
    ret += (handle * 5)

    return ret

for i in range(10):
    print i, alphabet[chr(ord('0')+i)]

vc = calculate_vc(666666 * 3 + 666666 * 5 + 666666 * 9, (1<<17) - 1, (1<<10) - 2, (1<<13) - 1, (1<<23) - 1, 1538329)
print num2str(str(vc))
