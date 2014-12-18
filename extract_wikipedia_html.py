#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, time, sys

#wikipediaのhtmlをクロールします
f1 = open("error_url", "w")

for abb_pair_list in open(sys.argv[1], "r"):
    target_title = abb_pair_list.strip().split(",")[0]
    write_text = "%s.txt" % target_title
    f = open(write_text, "w")
    url_text = "http://ja.wikipedia.org/wiki/%s" % target_title
    try:
        url = urllib2.urlopen(url_text).read()
    except:
        f1.write(url_text)
        continue
	"""except :
		f1.write(url_text)
        continue"""
    f.write(url)
    f.close()
    time.sleep(10.0)

f1.close()
