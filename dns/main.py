#!/usr/bin/env python
# coding=utf-8
import socket as s
import struct
import sys

server = s.socket(s.AF_INET, s.SOCK_DGRAM)
server.bind(('0.0.0.0', 53))

IP = '103.55.27.116'
pkgAddr = [ '{0:08b}'.format(int(x)) for x in IP.split('.')]

while True:
    streamData, addr = server.recvfrom(4096)
    data = []
    for s in streamData:
        b = struct.unpack("!B", s)[0]
        data.append('{0:08b}'.format(b))

    pkgID = data[:2]
    pkgFlag = ['10000001', '10000000']

    pkgQuery = ['00000000', '00000001']
    pkgAnswer = ['00000000', '00000001']

    pkgName = ['11000000', '00001100']
    pkgType = ['00000000', '00000001']
    pkgClass = ['00000000', '00000001']
    pkgTTL = ['00000000', '00000000', '00000101', '00010010']
    pkgLen = ['00000000', '00000100']

    binName = data[13:-5]
    domain = ''
    for i in binName:
        if int(i, 2) >= 96:
            domain += chr(int(i, 2))
        else:
	    domain += '.'


    print(domain + ' --> ' + IP)

    packet = pkgID + pkgFlag + pkgQuery + pkgAnswer +\
             data[8:] +\
	     pkgName + pkgType + pkgClass + pkgTTL + pkgLen + pkgAddr
    stream = ''
    for s in packet:
        stream += struct.pack("!B", int(s, 2))
    server.sendto(stream, addr)
