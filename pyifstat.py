#!/usr/bin/env python2
#-*- coding: utf-8 -*-
"""
网络带宽占用显示工具
"""
import time
import sys

if len(sys.argv) > 1:
    INTERFACE = sys.argv[1]
else:
    INTERFACE = 'eth0'
STATS = []
print 'Interface:',INTERFACE

def    rx():
    ifstat = open('/proc/net/dev').readlines()
    for interface in  ifstat:
        if INTERFACE in interface:
            stat = float(interface.split()[1])
            STATS[0:] = [stat]

def    tx():
    ifstat = open('/proc/net/dev').readlines()
    for interface in  ifstat:
        if INTERFACE in interface:
            stat = float(interface.split()[9])
            STATS[1:] = [stat]

def    main():
    rx()
    tx()

if __name__ == '__main__':
    main()

    print    'In/KB\t\tOut/KB'
    try:
        while    True:
            time.sleep(1)
            rxstat_o = list(STATS)
            main()
            RX = float(STATS[0])
            RX_O = rxstat_o[0]
            TX = float(STATS[1])
            TX_O = rxstat_o[1]
            RX_RATE = round((RX - RX_O)/1024,1)
            TX_RATE = round((TX - TX_O)/1024,1)
            print RX_RATE ,'\t\t',TX_RATE
    except KeyboardInterrupt:
        #break
        sys.exit()
