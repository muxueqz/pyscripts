#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys

class pinyin():
    def __init__(self, data_path='./Mandarin.dat'):
        self.dict = {}
        for line in open(data_path):
            k, v = line.split('\t')
            self.dict[k] = v
        self.splitter = ''
    def pinyin(self, chars):
        result = []
        for char in chars:
            key = "%X" % ord(char)
            try:
                result.append(self.dict[key].split(" ")[0].strip()[:-1].lower())
            except:
                result.append(char)
        return self.splitter.join(result)
if __name__ == "__main__":
    p = pinyin()
    s = '测试'
    #s = sys.argv[1]
    print unicode("%s",'utf8').encode('utf8') % s 
    us = unicode("%s").encode('utf8') % s 
#    ua = u"%s" % us
    print p.pinyin(u"测试")
    print p.pinyin("%s") % (us)
    #print p.pinyin(u"%s") % s
