#!/usr/bin/env python3
# coding=utf8
import ctypes

from PyQt5 import QtGui, QtCore
import sys

def inclip(data, target):
    app = QtGui.QGuiApplication(sys.argv)

    clipboard = app.clipboard()
    mimeData = QtCore.QMimeData()
    mimeData.setData(target, data.encode('utf8'))
    clipboard.setMimeData(mimeData)

    # important. let it wait for new clips (text & etc)
    # and only THEN die. otherwise on-the-fly conversion
    # to compatible TARGET will not work
    clipboard.dataChanged.connect(app.exit)

    app.exec()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '-in', '--input', default=True, action='store_true')
    parser.add_argument('-o', '-out', '--output', default=False, action='store_true')
    parser.add_argument('-silent', '--silent',
        default=True, action='store_true',
        help="errors only, run in background (default)"
    )
    parser.add_argument('-quiet', '--quiet',
        default=False, action='store_true',
        help="run in foreground, show what's happening"
    )

    parser.add_argument('-t', '-target', '--target', default='text/plain', type=str)

    args = parser.parse_args()

    data = sys.stdin.read()

    if args.quiet:
        args.silent = False

    if args.silent:
        ctypes.CDLL(None).daemon(0, 0)

    if args.input:
        inclip(data, args.target)
