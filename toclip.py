#!/usr/bin/env python3
# coding=utf8

from PyQt5 import QtGui, QtCore
import sys

def inclip(data, target):
    app = QtGui.QGuiApplication(sys.argv)

    clipboard = app.clipboard()
    mimeData = QtCore.QMimeData()
    # data = 'xx'
    # mimeData.setHtml(data)
    mimeData.setData(target, data.encode('utf8'))
    # mimeData.setText(data)
    clipboard.setMimeData(mimeData)

    # important. let it wait for new clips (text & etc)
    # and only THEN die. otherwise on-the-fly conversion
    # to compatible TARGET will not work
    clipboard.dataChanged.connect(app.exit)

    app.exec()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                     help='an integer for the accumulator')
    parser.add_argument('-i', '-in', '--input', default=True, action='store_true')
    parser.add_argument('-o', '-out', '--output', default=False, action='store_true')
    parser.add_argument('-t', '--target', default='text/plain', type=str)
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                     const=sum, default=max,
    #                     help='sum the integers (default: find the max)')

    args = parser.parse_args()
    # print(args.accumulate(args.key))
    print(args)

    data = sys.stdin.read()
    if args.input:
        inclip(data, args.target)
