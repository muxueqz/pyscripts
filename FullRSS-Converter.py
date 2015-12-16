#!/usr/bin/env python2
import urllib2
import sys

url = sys.argv[1][7:]

print 'http://fivefilters.org/content-only/makefulltextfeed.php?url=%s' % (urllib2.quote(url))
#print 'http://mrss.dokoda.jp/a/http/%s' % url
